from fastapi import APIRouter
from backend.app.api import auth, interview, report, analytics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(interview.router, prefix="/interview", tags=["interview"])
api_router.include_router(report.router, prefix="/report", tags=["report"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])


@api_router.get("/health")
async def health_check():
    return {"status": "ok", "message": "AI Interviewer Backend is running"}

