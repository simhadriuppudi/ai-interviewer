from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session
from backend.app.db import get_session
from backend.app.api import deps
from backend.app.services.scoring import analyze_performance
from backend.app.services.pdf_service import generate_pdf_report
from pydantic import BaseModel

router = APIRouter()

class ReportRequest(BaseModel):
    conversation: list # List of {role: str, content: str}

@router.post("/generate")
async def generate_report(
    req: ReportRequest,
    current_user = Depends(deps.get_current_user)
):
    try:
        report = await analyze_performance(req.conversation)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download")
async def download_report(
    req: ReportRequest,
    current_user = Depends(deps.get_current_user)
):
    try:
        report = await analyze_performance(req.conversation)
        pdf_bytes = generate_pdf_report(report)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
