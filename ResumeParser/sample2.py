import sys
import pdfplumber
from docx import Document
import spacy
from spacy.matcher import Matcher
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import os
import subprocess
import logging
from fuzzywuzzy import fuzz
import pytesseract
from PIL import Image
import io
import streamlit as st
try:
    from docling.document_converter import DocumentConverter
except ImportError:
    DocumentConverter = None

# Set up logging
logging.basicConfig(
    filename='resume_parser.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize spaCy and NLTK
nlp = spacy.load("en_core_web_sm")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Comprehensive skills database (simplified, can be loaded from JSON)
SKILLS_DB = [
    "python", "java", "javascript", "sql", "machine learning", "data analysis",
    "project management", "aws", "docker", "git", "excel", "tableau",
    "communication", "leadership", "problem solving", "tensorflow", "kubernetes",
    "react", "node.js", "c", "flask", "linux", "pandas", "mysql", "mongodb",
    "numpy", "scikit-learn", "django", "sql server", "fastapi", "pytorch"
]

# Common locations for address validation (simplified gazetteer)
LOCATIONS = {
    "india", "bangalore", "bengaluru", "mumbai", "uk", "canada", "europe", "us",
    "africa", "fremont", "london", "new york", "california", "karnataka"
}

def extract_text_from_file(file_path: str, use_docling_for_pdf: bool = False) -> str:
    """Extract text from a PDF, DOCX, or DOC file with OCR fallback."""
    file_ext = os.path.splitext(file_path)[1].lower()
    logging.info(f"Processing file: {file_path} (extension: {file_ext})")
    
    try:
        if file_ext == ".pdf":
            if use_docling_for_pdf and DocumentConverter is not None:
                converter = DocumentConverter()
                doc = converter.convert(file_path)
                text = doc.text if hasattr(doc, 'text') else str(doc)
                logging.info("Extracted text with docling")
                return text
            else:
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                        else:
                            # Fallback to OCR for scanned PDFs
                            img = page.to_image().original
                            text += pytesseract.image_to_string(img) + "\n"
                    logging.info("Extracted text with pdfplumber/OCR")
                    return text
        elif file_ext == ".docx":
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs if para.text])
            logging.info("Extracted text with python-docx")
            return text
        elif file_ext == ".doc":
            result = subprocess.run(["antiword", file_path], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("Extracted text with antiword")
                return result.stdout
            else:
                raise ValueError(f"antiword failed: {result.stderr}")
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

def extract_name(doc: spacy.tokens.Doc) -> str:
    """Extract name using spaCy's NER with validation."""
    exclude_terms = {
        "india", "bangalore", "bengaluru", "mumbai", "savari", "uk", "canada", "europe",
        "us", "africa", "fremont", "highlighting", "supporting", "employee", "maintaining",
        "l-1b", "h-1b", "h-2b", "po", "europe global mobility", "handling request",
        "extensive experience", "global mobility", "immigration", "international assignments",
        "europe countries", "summary", "objective", "profile"
    }
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.text.lower() not in exclude_terms:
            # Validate multi-word names or initials
            if len(ent.text.split()) >= 2 or re.match(r"^[A-Za-z]+\s[A-Z]\.?\s[A-Za-z]+$", ent.text):
                logging.info(f"Extracted name: {ent.text}")
                return ent.text
    # Fallback: Regex with validation
    lines = doc.text.split("\n")
    for line in lines[:5]:
        line = line.strip()
        if (line and re.match(r"^[A-Za-z]+(\s[A-Za-z]+)+([.-][A-Za-z]+)*$", line) 
                and line.lower() not in exclude_terms and len(line.split()) <= 4):
            logging.info(f"Extracted name (regex): {line}")
            return line
    logging.warning("No name extracted")
    return None

def extract_address(doc: spacy.tokens.Doc) -> str:
    """Extract address using spaCy's NER and regex with validation."""
    non_address_terms = {
        "c", "flask", "linux", "savari", "python", "java", "javascript", "sql", "tableauau",
        "mysql", "mongodb", "javascript", "supporting", "mysql", "javascript", "javascript",
        "employee", "javascript", "maintaining", "l-1b", "javascript", "javascript",
        "h-1b", "h-2b", "po", "javascript", "europe", "javascript", "global",
        "extensive", "experience", "extensive", "javascript", "global",
 "javascript",
        "immigration", "migration", "international", "international",
 "javascript", "europe",
 "javascript", "countries", "javascript",
    }
    addresses = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "HOC"] and ent.text.lower() not in non_address_terms:
            # Validate against locations gazetteer
            if ent.text.lower() in LOCATIONS:
                addresses.append(ent.text)
    # Multiple address regex patterns
    address_patterns = [
        re.compile(r"\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[A-Za-z\s]+\s\d{6}"),  # Indian
        # re.compile(r"\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[A-Z]{2}\s\d{5}"),     # US
        # re.compile(r"[\w\s]+,\s[A-Za-z\s]+,\s[A-Za-z\s]+"),              # General
        # re.compile(r"[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}")                   # UK
    ]
    for pattern in address_patterns:
        match = pattern.search(doc.text)
        if match:
            addresses.append(match.group())
    addresses = list(set(addresses))
    if addresses:
        logging.info(f" extracted address: {addresses}")
        return ", ".join(addresses)
    logging.warning("Address not found")
    return addresses

def extract_skills(doc: spacy.tokens.Doc, skills_db: str = SKILLS_DB) -> list[str]:
    """Extract skills using spaCy's Matcher, NLTK, and fuzzy matching."""
    matcher = Matcher(nlp.vocab)
    for skill in skills_db:
        pattern = [{"LOWER": {"LOWER": word.lower()}} for word in skill.split()]
        matcher.add(skill, [pattern], [pattern])
    
    matches = matcher(doc)
    found_skills = set()
    for match_id, start, end in matches:
        skill = doc[start:end].text.lower()
        found_skills.add(skill.lower())
    
    # Normalize text for fuzzy matching
    normalized_text = re.sub(r'[^\w\s]', '', doc.text.lower())
    tokens = word_tokenize(normalized_text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Fuzzy matching for skills variations
    for skill in skills_db:
        skill_words = skill.lower().split()
        if all(word in tokens for word in skill_words):
            found_skills.add(skill.lower())
        elif any(fuzz.ratio(skill.lower(), token) > 80 for token in tokens):
            found_skills.add(skill.lower())
    
    logging.info(f"Extracted skills: {found_skills}")
    return list(found_skills)

def parse_resume(file_path: str, use_docling_for_pdf: bool = False) -> dict:
    """Parse resume and extract name, skills, and address."""
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return {"error": f"File not found: {file_path}"}
    
    text = extract_text_from_file(file_path, use_docling_for_pdf)
    if not text:
        logging.error("Failed to extract text from file")
        return {"error": "Failed to extract text from file"}
    
    doc = nlp(text)
    
    result = {
        "name": extract_name(doc),
        "address": extract_address(doc),
        "skills": extract_skills(doc)
    }
    logging.info(f"Parsed resume: {result}")
    return result

def streamlit_app():
    """Streamlit UI for resume parsing."""
    st.title("Resume Parser")
    uploaded_file = st.file_uploader("Upload Resume (.pdf, .docx, .doc)", type=["pdf", "docx", "doc"])
    
    if uploaded_file:
        with open("temp_resume", "wb") as f:
            f.write(uploaded_file.getbuffer())
        result = parse_resume("temp_resume")
        os.remove("temp_resume")
        
        st.subheader("Extracted Resume Details")
        st.write(f"**Name**: {result.get('name', 'Not found')}")
        st.write(f"**Address**: {result.get('address', 'Not found')}")
        st.write(f"**Skills**: {', '.join(result.get('skills', ['Not found']))}")
        
        # Download results as JSON
        st.download_button(
            label="Download Results",
            data=str(result),
            file_name="resume_details.json",
            mime="application/json"
        )

if __name__ == "__main__":
    if 'streamlit' in sys.argv:
        streamlit_app()
    else:
        resume_path = "/home/kamal/Documents/1.Git/BloomWS/ResumeParser/resume.doc"  # Update path
        result = parse_resume(resume_path, use_docling_for_pdf=False)
        print("Extracted Resume Details:")
        print(f"Name: {result.get('name', 'Not found')}")
        print(f"Address: {result.get('address', 'Not found')}")
        print(f"Skills: {result.get('skills', 'Not found')}")
