from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Voice-Enabled AI Interviewer"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./interview.db"
    SECRET_KEY: str = "changethis" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Gemini API
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3-flash-preview"
    
    # Interview Configuration
    DEFAULT_INTERVIEW_DURATION: int = 30
    MAX_QUESTIONS_PER_INTERVIEW: int = 10

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
