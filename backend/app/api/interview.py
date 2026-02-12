from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
from pathlib import Path

from backend.app.db import get_session
from backend.app.api import deps
from backend.app.models.user import User
from backend.app.models.interview import InterviewHistory, InterviewQuestion, PerformanceMetric
from backend.app.services.parser import parse_resume
from backend.app.services.rag import rag_engine
from backend.app.services.gemini_service import gemini_client
from backend.app.services.voice_service import voice_service

router = APIRouter()

# Request/Response Models
class InterviewSetupRequest(BaseModel):
    job_description: str
    interview_types: List[str]  # ["HR", "Technical", "Aptitude"]

class InterviewStartResponse(BaseModel):
    interview_id: int
    first_question: str
    audio_base64: Optional[str] = None

class AnswerRequest(BaseModel):
    interview_id: int
    answer: str

class AnswerResponse(BaseModel):
    next_question: Optional[str] = None
    audio_base64: Optional[str] = None
    is_complete: bool = False

class EndInterviewResponse(BaseModel):
    interview_id: int
    performance_report: dict

# Global storage for current interview context (in production, use Redis or similar)
interview_contexts = {}

@router.post("/setup")
async def setup_interview(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    interview_types: str = Form(...),  # Comma-separated: "HR,Technical"
    current_user: User = Depends(deps.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Upload resume and job description to set up interview
    """
    # Parse interview types
    types_list = [t.strip() for t in interview_types.split(",")]
    
    # Save resume file
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    # Use timestamp without colons for Windows compatibility
    timestamp = str(int(datetime.utcnow().timestamp()))
    resume_filename = f"{current_user.id}_{timestamp}_{resume.filename}"
    resume_path = upload_dir / resume_filename
    
    # Read and save resume file
    resume_bytes = await resume.read()
    with open(resume_path, "wb") as f:
        f.write(resume_bytes)
    
    # Parse resume content
    resume_content = await parse_resume(resume_bytes, resume.filename)
    
    if not resume_content:
        raise HTTPException(status_code=400, detail="Could not parse resume file.")

    
    # Clear and populate RAG engine
    rag_engine.clear()
    rag_engine.add_document(resume_content)
    rag_engine.add_document(job_description)
    
    # Create interview record
    interview = InterviewHistory(
        user_id=current_user.id,
        interview_type=",".join(types_list),
        resume_path=str(resume_path),
        job_description=job_description,
        status="ready"
    )
    
    session.add(interview)
    session.commit()
    session.refresh(interview)
    
    # Store context for this interview
    interview_contexts[interview.id] = {
        "resume": resume_content,
        "job_description": job_description,
        "types": types_list,
        "current_type_index": 0,
        "question_count": 0
    }
    
    return {
        "status": "ready",
        "interview_id": interview.id,
        "message": "Interview context set successfully."
    }

@router.post("/start", response_model=InterviewStartResponse)
async def start_interview(
    interview_id: int,
    current_user: User = Depends(deps.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Start the interview and get the first question
    """
    # Get interview
    interview = session.get(InterviewHistory, interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Update status
    interview.status = "in_progress"
    interview.started_at = datetime.utcnow()
    session.add(interview)
    session.commit()
    
    # Get context
    context = interview_contexts.get(interview_id)
    if not context:
        raise HTTPException(status_code=400, detail="Interview context not found. Please setup again.")
    
    # Generate first question
    interview_type = context["types"][0]
    context_str = f"Resume:\n{context['resume']}\n\nJob Description:\n{context['job_description']}"
    
    first_question = gemini_client.generate_interview_question(
        context=context_str,
        interview_type=interview_type,
        previous_qa=None
    )
    
    # Save question to database
    question_record = InterviewQuestion(
        interview_id=interview_id,
        question_number=1,
        question_text=first_question
    )
    session.add(question_record)
    session.commit()
    
    # Generate TTS audio (with error handling)
    audio_base64 = ""
    try:
        audio_base64 = voice_service.text_to_speech_base64(first_question)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"TTS generation failed: {e}")
        # Continue without audio
    
    return InterviewStartResponse(
        interview_id=interview_id,
        first_question=first_question,
        audio_base64=audio_base64
    )

@router.post("/answer", response_model=AnswerResponse)
async def submit_answer(
    answer_req: AnswerRequest,
    current_user: User = Depends(deps.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Submit answer and get next question
    """
    interview = session.get(InterviewHistory, answer_req.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Get the last unanswered question
    statement = select(InterviewQuestion).where(
        InterviewQuestion.interview_id == answer_req.interview_id,
        InterviewQuestion.answer_text == None
    ).order_by(InterviewQuestion.question_number.desc())
    
    last_question = session.exec(statement).first()
    
    if not last_question:
        raise HTTPException(status_code=400, detail="No pending question found")
    
    # Save answer
    last_question.answer_text = answer_req.answer
    last_question.answered_at = datetime.utcnow()
    session.add(last_question)
    session.commit()
    
    # Get context
    context = interview_contexts.get(answer_req.interview_id)
    if not context:
        raise HTTPException(status_code=400, detail="Interview context not found")
    
    context["question_count"] += 1
    
    # No question limit - allow unlimited questions
    # Users can end interview manually when ready
    
    
    # Get all previous Q&A
    all_questions = session.exec(
        select(InterviewQuestion).where(
            InterviewQuestion.interview_id == answer_req.interview_id
        ).order_by(InterviewQuestion.question_number)
    ).all()
    
    previous_qa = [
        {"question": q.question_text, "answer": q.answer_text}
        for q in all_questions if q.answer_text
    ]
    
    # Generate next question
    current_type = context["types"][context["current_type_index"]]
    context_str = f"Resume:\n{context['resume']}\n\nJob Description:\n{context['job_description']}"
    
    next_question = gemini_client.generate_interview_question(
        context=context_str,
        interview_type=current_type,
        previous_qa=previous_qa
    )
    
    # Save next question
    question_record = InterviewQuestion(
        interview_id=answer_req.interview_id,
        question_number=len(all_questions) + 1,
        question_text=next_question
    )
    session.add(question_record)
    session.commit()
    
    # Generate TTS (with error handling)
    audio_base64 = ""
    try:
        audio_base64 = voice_service.text_to_speech_base64(next_question)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"TTS generation failed in answer endpoint: {e}")
        # Continue without audio
    
    return AnswerResponse(
        next_question=next_question,
        audio_base64=audio_base64,
        is_complete=False
    )

@router.post("/end", response_model=EndInterviewResponse)
async def end_interview(
    interview_id: int,
    current_user: User = Depends(deps.get_current_user),
    session: Session = Depends(get_session)
):
    """
    End interview and generate performance report
    """
    interview = session.get(InterviewHistory, interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Update interview status
    interview.status = "completed"
    interview.ended_at = datetime.utcnow()
    session.add(interview)
    
    # Get all Q&A
    questions = session.exec(
        select(InterviewQuestion).where(
            InterviewQuestion.interview_id == interview_id
        ).order_by(InterviewQuestion.question_number)
    ).all()
    
    qa_list = [
        {"question": q.question_text, "answer": q.answer_text or ""}
        for q in questions
    ]
    
    # Get context
    context = interview_contexts.get(interview_id, {})
    context_str = f"Resume:\n{context.get('resume', '')}\n\nJob Description:\n{context.get('job_description', '')}"
    
    # Generate performance report using Gemini
    report = gemini_client.generate_performance_report(
        questions_answers=qa_list,
        context=context_str,
        interview_type=interview.interview_type
    )
    
    # Save performance metrics
    performance = PerformanceMetric(
        interview_id=interview_id,
        overall_score=report.get("overall_score", 50),
        accuracy_score=report.get("accuracy_score", 5),
        clarity_score=report.get("clarity_score", 5),
        confidence_score=report.get("confidence_score", 5),
        summary=report.get("summary", "")
    )
    performance.set_strengths(report.get("strengths", []))
    performance.set_weaknesses(report.get("weaknesses", []))
    performance.set_improvements(report.get("improvements", []))
    
    session.add(performance)
    session.commit()
    session.refresh(performance)
    
    # Get previous interviews for comparison
    previous_interviews = session.exec(
        select(InterviewHistory).where(
            InterviewHistory.user_id == current_user.id,
            InterviewHistory.id != interview_id,
            InterviewHistory.status == "completed"
        ).order_by(InterviewHistory.ended_at.desc())
    ).all()
    
    comparison = None
    if previous_interviews:
        prev_interview = previous_interviews[0]
        prev_performance = session.exec(
            select(PerformanceMetric).where(
                PerformanceMetric.interview_id == prev_interview.id
            )
        ).first()
        
        if prev_performance:
            comparison = {
                "previous_score": prev_performance.overall_score,
                "current_score": performance.overall_score,
                "improvement": performance.overall_score - prev_performance.overall_score,
                "previous_date": prev_interview.ended_at.isoformat() if prev_interview.ended_at else None
            }
    
    # Build complete report
    complete_report = {
        **report,
        "strengths": performance.get_strengths(),
        "weaknesses": performance.get_weaknesses(),
        "improvements": performance.get_improvements(),
        "comparison": comparison
    }
    
    return EndInterviewResponse(
        interview_id=interview_id,
        performance_report=complete_report
    )

@router.get("/tts/{text}")
async def get_tts_audio(text: str):
    """
    Generate TTS audio for given text
    """
    audio_base64 = voice_service.text_to_speech_base64(text)
    return {"audio_base64": audio_base64}
