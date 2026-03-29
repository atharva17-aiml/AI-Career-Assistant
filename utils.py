import fitz
from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    try:
        # Try PyMuPDF first
        text = ""
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
        return text
    
    except:
        try:
            # Fallback to PyPDF2
            file.seek(0)
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        
        except Exception as e:
            return f"ERROR: Could not read PDF ({str(e)})"