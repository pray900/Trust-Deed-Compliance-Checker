# pdf_parser.py
import fitz
import re
 
def extract_clauses(pdf_file): # Notice the argument is now the file object
    # Read the file from Streamlit's memory
    file_bytes = pdf_file.read()
    # Open the PDF using the raw byte stream instead of a file path
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = " ".join([page.get_text() for page in doc])
 
    # Split on legal clause patterns: 1. / 1.1 / (a) / CLAUSE 1
    clause_pattern = r'(?=\b\d+\.\d*\s|\b[A-Z]{2,}\s\d+\.|\([a-z]\)\s)'
    clauses = re.split(clause_pattern, full_text)
    clauses = [c.strip() for c in clauses if len(c.strip()) > 40]
    return clauses