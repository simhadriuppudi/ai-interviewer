#!/usr/bin/env python3
"""
Startup script for Render deployment with enhanced error handling and logging
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check required environment variables"""
    required_vars = ['GEMINI_API_KEY', 'SECRET_KEY', 'DATABASE_URL']
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
            logger.error(f"Missing environment variable: {var}")
        else:
            logger.info(f"✓ {var} is set")
    
    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        return False
    return True

def main():
    """Main startup function"""
    logger.info("=" * 60)
    logger.info("Starting AI Interviewer Application")
    logger.info("=" * 60)
    
    # Check Python version
    logger.info(f"Python version: {sys.version}")
    
    # Check environment variables
    logger.info("Checking environment variables...")
    if not check_environment():
        logger.error("Environment check failed!")
        sys.exit(1)
    
    # Get port from environment
    port = int(os.getenv('PORT', 8000))
    logger.info(f"PORT environment variable: {port}")
    
    # Check if we can import required modules
    logger.info("Checking imports...")
    try:
        import fastapi
        logger.info(f"✓ FastAPI version: {fastapi.__version__}")
        
        import uvicorn
        logger.info(f"✓ Uvicorn version: {uvicorn.__version__}")
        
        import google.generativeai as genai
        logger.info("✓ Google Generative AI imported successfully")
        
        from backend.app.main import app
        logger.info("✓ Application imported successfully")
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        sys.exit(1)
    
    # Start the server
    logger.info("=" * 60)
    logger.info(f"Starting Uvicorn server on 0.0.0.0:{port}")
    logger.info("=" * 60)
    
    try:
        uvicorn.run(
            "backend.app.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
