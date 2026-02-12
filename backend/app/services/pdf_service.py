from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import json

def generate_pdf_report(report_data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "AI Interviewer Performance Report")
    
    # Scores
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 100, "Scores Overview")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 130, f"Overall Score: {report_data.get('overall_score', 'N/A')}")
    c.drawString(50, height - 150, f"Clarity Grade: {report_data.get('clarity_grade', 'N/A')}")
    c.drawString(50, height - 170, f"Confidence Level: {report_data.get('confidence_level', 'N/A')}")
    
    # Feedback
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 220, "Detailed Feedback")
    
    y = height - 250
    c.setFont("Helvetica", 12)
    
    feedback_list = report_data.get('key_feedback', [])
    for item in feedback_list:
        if y < 100:
            c.showPage()
            y = height - 50
            
        title = item.get('title', 'Point')
        desc = item.get('description', '')
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"- {title}")
        y -= 20
        
        c.setFont("Helvetica", 10)
        # Simple text wrapping logic (very basic)
        max_char = 90
        start = 0
        while start < len(desc):
            line = desc[start:start+max_char]
            c.drawString(70, y, line)
            y -= 15
            start += max_char
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
