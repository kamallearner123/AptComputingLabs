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
try:
    from docling.document_converter import DocumentConverter
except ImportError:
    DocumentConverter = None

# Initialize spaCy and NLTK
nlp = spacy.load("en_core_web_sm")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Expanded list of skills
SKILLS = [
    "python", "java", "javascript", "sql", "machine learning", "data analysis",
    "project management", "aws", "docker", "git", "excel", "tableau",
    "communication", "leadership", "problem solving", "tensorflow", "kubernetes",
    "react", "node.js", "c", "flask", "linux", "pandas", "mysql", "mongodb",
    "numpy", "scikit-learn", "django", "sql server"
]

def extract_text_from_file(file_path, use_docling_for_pdf=False):
    """Extract text from a PDF, DOCX, or DOC file."""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == ".pdf":
            if use_docling_for_pdf and DocumentConverter is not None:
                converter = DocumentConverter()
                doc = converter.convert(file_path)
                text = doc.text if hasattr(doc, 'text') else str(doc)
                return text
            else:
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    return text
        elif file_ext == ".docx":
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs if para.text])
            return text
        elif file_ext == ".doc":
            result = subprocess.run(["antiword", file_path], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                raise ValueError(f"antiword failed: {result.stderr}")
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def extract_name(doc):
    """Extract name using spaCy's NER (PERSON entity) or regex."""
    exclude_terms = {
        "india", "bangalore", "bengaluru", "mumbai", "savari", "uk", "canada", "europe",
        "us", "africa", "fremont", "highlighting", "supporting", "employee", "maintaining",
        "l-1b", "h-1b", "h-2b", "po", "europe global mobility", "handling request",
        "extensive experience", "global mobility", "immigration", "international assignments",
        "europe countries"
    }
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.text.lower() not in exclude_terms:
            # Ensure multi-word name or initials (e.g., "John Doe", "Jane M. Smith")
            if len(ent.text.split()) >= 2 or re.match(r"^[A-Za-z]+\s[A-Z]\.?\s[A-Za-z]+$", ent.text):
                return ent.text
    # Fallback: Stricter regex for names
    lines = doc.text.split("\n")
    for line in lines[:5]:
        line = line.strip()
        if line and re.match(r"^[A-Za-z]+(\s[A-Za-z]+)+([.-][A-Za-z]+)*$", line) and line.lower() not in exclude_terms:
            return line
    return None

def extract_address(doc):
    """Extract address using spaCy's NER (GPE or LOC) or regex."""
    non_address_terms = {
        "c", "flask", "linux", "savari", "python", "java", "javascript", "sql", "tableau",
        "mysql", "mongodb", "supporting", "employee", "maintaining", "l-1b", "h-1b", "h-2b",
        "po", "europe global mobility", "extensive experience", "global mobility",
        "immigration", "international assignments", "europe countries"
    }
    addresses = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"] and ent.text.lower() not in non_address_terms:
            addresses.append(ent.text)
    # Regex for global addresses
    address_patterns = [
        re.compile(r"\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[A-Za-z\s]+\s\d{6}"),  # Indian: "123 Main Road, Bengaluru, Karnataka 560001"
        re.compile(r"\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[A-Z]{2}\s\d{5}"),     # US: "123 Main St, Springfield, IL 62701"
        re.compile(r"[\w\s]+,\s[A-Za-z\s]+,\s[A-Za-z\s]+"),              # General: "London, England, UK"
        re.compile(r"[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}")                   # UK: "SW1A 1AA"
    ]
    for pattern in address_patterns:
        match = pattern.search(doc.text)
        if match:
            addresses.append(match.group())
    return ", ".join(set(addresses)) if addresses else None

def extract_skills(doc, skills_list=SKILLS):
    """Extract skills using spaCy's Matcher and NLTK preprocessing."""
    matcher = Matcher(nlp.vocab)
    for skill in skills_list:
        pattern = [{"LOWER": word.lower()} for word in skill.split()]
        matcher.add(skill, [pattern])
    
    matches = matcher(doc)
    found_skills = set()
    for match_id, start, end in matches:
        skill = doc[start:end].text.lower()
        found_skills.add(skill)
    
    # Normalize text for broader keyword search
    normalized_text = re.sub(r'[^\w\s]', '', doc.text.lower())
    tokens = word_tokenize(normalized_text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    for skill in skills_list:
        skill_words = skill.lower().split()
        if all(word in tokens for word in skill_words):
            found_skills.add(skill.lower())
    
    data_skills = list(found_skills)
    return ":".join(data_skills)

def parse_resume(file_path, use_docling_for_pdf=False):
    """Parse resume and extract name, skills, and address."""
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    text = extract_text_from_file(file_path, use_docling_for_pdf)
    if not text:
        return {"error": "Failed to extract text from file"}
    
    doc = nlp(text)
    
    result = {
        "name": extract_name(doc).replace(',', ' '),
        "address": extract_address(doc).replace(',', ' '),
        "skills": extract_skills(doc).replace(',', ' ')
    }
    return result