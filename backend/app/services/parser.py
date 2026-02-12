import PyPDF2
from docx import Document
import io

async def parse_pdf(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

async def parse_docx(file_bytes: bytes) -> str:
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        return ""

async def parse_resume(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        return await parse_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        return await parse_docx(file_bytes)
    else:
        # Try as plain text
        try:
            return file_bytes.decode('utf-8')
        except:
            return ""
