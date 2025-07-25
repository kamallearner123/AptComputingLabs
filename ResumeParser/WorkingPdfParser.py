import pdfplumber
from docx import Document
import spacy
from spacy.matcher import Matcher
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import os
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
    "react", "node.js", "c", "flask", "linux"
]

def extract_text_from_file(file_path, use_docling_for_pdf=False):
    """Extract text from a PDF or DOCX file."""
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
            raise ValueError("Legacy .doc files are not supported. Convert to .docx or .pdf using LibreOffice or Microsoft Word.")
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def extract_name(doc):
    """Extract name using spaCy's NER (PERSON entity) or regex."""
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not any(ent.text.lower() in ["india", "bangalore", "bengaluru", "mumbai"] for ent in doc.ents):
            return ent.text
    # Fallback: Stricter regex for names (e.g., "John Doe", "Jane M. Smith")
    lines = doc.text.split("\n")
    for line in lines[:5]:
        line = line.strip()
        if line and re.match(r"^[A-Za-z]+(\s[A-Za-z]+)+([.-][A-Za-z]+)*$", line):
            return line
    return None

def extract_address(doc):
    """Extract address using spaCy's NER (GPE or LOC) or regex."""
    # Known non-address terms to filter
    non_address_terms = {"c", "flask", "linux", "savari", "python", "java", "javascript", "sql", "tableau"}
    addresses = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"] and ent.text.lower() not in non_address_terms:
            addresses.append(ent.text)
    # Regex for US-style addresses (extend for other formats if needed)
    address_pattern = re.compile(r"\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[A-Z]{2}\s\d{5}")
    match = address_pattern.search(doc.text)
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
    
    tokens = word_tokenize(doc.text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    for skill in skills_list:
        if skill.lower() in tokens:
            found_skills.add(skill.lower())
    
    return list(found_skills)

def parse_resume(file_path, use_docling_for_pdf=False):
    """Parse resume and extract name, skills, and address."""
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    text = extract_text_from_file(file_path, use_docling_for_pdf)
    if not text:
        return {"error": "Failed to extract text from file"}
    
    doc = nlp(text)
    
    result = {
        "name": extract_name(doc),
        "address": extract_address(doc),
        "skills": extract_skills(doc)
    }
    return result

if __name__ == "__main__":
    resume_path = "/home/kamal/Documents/1.Git/BloomWS/ResumeParser/resume.pdf"  # Replace with your resume file path (.pdf or .docx)
    result = parse_resume(resume_path, use_docling_for_pdf=False)
    print("Extracted Resume Details:")
    print(f"Name: {result.get('name', 'Not found')}")
    print(f"Address: {result.get('address', 'Not found')}")
    print(f"Skills: {result.get('skills', 'Not found')}")
