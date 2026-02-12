from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import json

class InterviewHistory(SQLModel, table=True):
    """Store complete interview sessions"""
    __tablename__ = "interview_history"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    interview_type: str  # HR, Technical, Aptitude
    resume_path: Optional[str] = None
    job_description: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    status: str = "in_progress"  # in_progress, completed, abandoned
    
    # Relationships
    questions: List["InterviewQuestion"] = Relationship(back_populates="interview")
    performance: Optional["PerformanceMetric"] = Relationship(back_populates="interview")

class InterviewQuestion(SQLModel, table=True):
    """Individual questions and answers in an interview"""
    __tablename__ = "interview_question"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    interview_id: int = Field(foreign_key="interview_history.id")
    question_number: int
    question_text: str
    answer_text: Optional[str] = None
    asked_at: datetime = Field(default_factory=datetime.utcnow)
    answered_at: Optional[datetime] = None
    
    # Relationship
    interview: Optional[InterviewHistory] = Relationship(back_populates="questions")

class PerformanceMetric(SQLModel, table=True):
    """Scoring and analytics data for interviews"""
    __tablename__ = "performance_metric"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    interview_id: int = Field(foreign_key="interview_history.id", unique=True)
    overall_score: float  # 0-100
    accuracy_score: float  # 0-10
    clarity_score: float  # 0-10
    confidence_score: float  # 0-10
    strengths: str  # JSON array
    weaknesses: str  # JSON array
    improvements: str  # JSON array
    summary: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    interview: Optional[InterviewHistory] = Relationship(back_populates="performance")
    
    def get_strengths(self) -> list:
        """Parse strengths from JSON string"""
        try:
            return json.loads(self.strengths) if self.strengths else []
        except:
            return []
    
    def set_strengths(self, strengths_list: list):
        """Set strengths as JSON string"""
        self.strengths = json.dumps(strengths_list)
    
    def get_weaknesses(self) -> list:
        """Parse weaknesses from JSON string"""
        try:
            return json.loads(self.weaknesses) if self.weaknesses else []
        except:
            return []
    
    def set_weaknesses(self, weaknesses_list: list):
        """Set weaknesses as JSON string"""
        self.weaknesses = json.dumps(weaknesses_list)
    
    def get_improvements(self) -> list:
        """Parse improvements from JSON string"""
        try:
            return json.loads(self.improvements) if self.improvements else []
        except:
            return []
    
    def set_improvements(self, improvements_list: list):
        """Set improvements as JSON string"""
        self.improvements = json.dumps(improvements_list)
