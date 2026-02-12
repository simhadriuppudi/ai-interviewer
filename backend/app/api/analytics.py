from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from backend.app.db import get_session
from backend.app.api import deps
from backend.app.models.user import User
from backend.app.models.interview import InterviewHistory, PerformanceMetric, InterviewQuestion
from pydantic import BaseModel

router = APIRouter()

class InterviewHistoryResponse(BaseModel):
    id: int
    interview_type: str
    started_at: datetime
    ended_at: datetime | None
    status: str
    overall_score: float | None

class PerformanceReportResponse(BaseModel):
    interview_id: int
    overall_score: float
    accuracy_score: float
    clarity_score: float
    confidence_score: float
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]
    summary: str | None
    interview_date: datetime | None

@router.get("/history", response_model=List[InterviewHistoryResponse])
async def get_interview_history(
    current_user: User = Depends(deps.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all interview history for the current user
    """
    interviews = session.exec(
        select(InterviewHistory).where(
            InterviewHistory.user_id == current_user.id
        ).order_by(InterviewHistory.started_at.desc())
    ).all()
    
    result = []
    for interview in interviews:
        # Get performance metric if exists
        performance = session.exec(
            select(PerformanceMetric).where(
                PerformanceMetric.interview_id == interview.id
            )
        ).first()
        
        result.append(InterviewHistoryResponse(
            id=interview.id,
            interview_type=interview.interview_type,
            started_at=interview.started_at,
            ended_at=interview.ended_at,
            status=interview.status,
            overall_score=performance.overall_score if performance else None
        ))
    
    return result

@router.get("/report/{interview_id}", response_model=PerformanceReportResponse)
async def get_performance_report(
    interview_id: int,
    current_user: User = Depends(deps.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get detailed performance report for a specific interview
    """
    interview = session.get(InterviewHistory, interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    performance = session.exec(
        select(PerformanceMetric).where(
            PerformanceMetric.interview_id == interview_id
        )
    ).first()
    
    if not performance:
        raise HTTPException(status_code=404, detail="Performance report not found")
    
    return PerformanceReportResponse(
        interview_id=interview_id,
        overall_score=performance.overall_score,
        accuracy_score=performance.accuracy_score,
        clarity_score=performance.clarity_score,
        confidence_score=performance.confidence_score,
        strengths=performance.get_strengths(),
        weaknesses=performance.get_weaknesses(),
        improvements=performance.get_improvements(),
        summary=performance.summary,
        interview_date=interview.ended_at
    )

@router.get("/comparison")
async def get_performance_comparison(
    current_user: User = Depends(deps.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Compare performance across all completed interviews
    """
    interviews = session.exec(
        select(InterviewHistory).where(
            InterviewHistory.user_id == current_user.id,
            InterviewHistory.status == "completed"
        ).order_by(InterviewHistory.ended_at.desc())
    ).all()
    
    if len(interviews) < 2:
        return {
            "message": "Need at least 2 completed interviews for comparison",
            "interviews_count": len(interviews)
        }
    
    # Get performance metrics for all interviews
    comparisons = []
    for i, interview in enumerate(interviews):
        performance = session.exec(
            select(PerformanceMetric).where(
                PerformanceMetric.interview_id == interview.id
            )
        ).first()
        
        if performance:
            comparisons.append({
                "interview_number": len(interviews) - i,
                "date": interview.ended_at.isoformat() if interview.ended_at else None,
                "interview_type": interview.interview_type,
                "overall_score": performance.overall_score,
                "accuracy_score": performance.accuracy_score,
                "clarity_score": performance.clarity_score,
                "confidence_score": performance.confidence_score
            })
    
    # Calculate improvements
    if len(comparisons) >= 2:
        latest = comparisons[0]
        previous = comparisons[1]
        
        improvements = {
            "overall": latest["overall_score"] - previous["overall_score"],
            "accuracy": latest["accuracy_score"] - previous["accuracy_score"],
            "clarity": latest["clarity_score"] - previous["clarity_score"],
            "confidence": latest["confidence_score"] - previous["confidence_score"]
        }
    else:
        improvements = None
    
    return {
        "interviews": comparisons,
        "improvements": improvements,
        "total_interviews": len(comparisons)
    }
