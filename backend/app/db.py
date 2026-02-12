from sqlmodel import SQLModel, create_engine, Session
from backend.app.core.config import settings

# Import all models to ensure they're registered with SQLModel
from backend.app.models.user import User
from backend.app.models.interview import InterviewHistory, InterviewQuestion, PerformanceMetric

# check_same_thread=False is needed for SQLite
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False}
)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize database and create all tables"""
    SQLModel.metadata.create_all(engine)
