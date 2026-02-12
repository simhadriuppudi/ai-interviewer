#!/usr/bin/env python3
"""
Startup script for Render deployment with enhanced error handling and logging
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check required environment variables"""
    required_vars = ['SECRET_KEY']
    optional_vars = ['GEMINI_API_KEY', 'DATABASE_URL']
    
    logger.info("Checking environment variables...")
    
    missing_required = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_required.append(var)
            logger.error(f"✗ Missing REQUIRED: {var}")
        else:
            logger.info(f"✓ {var} is set")
    
    for var in optional_vars:
        value = os.getenv(var)
        if not value:
            logger.warning(f"⚠ Missing optional: {var}")
        else:
            logger.info(f"✓ {var} is set")
    
    if missing_required:
        logger.error(f"Missing required environment variables: {', '.join(missing_required)}")
        return False
    return True

def main():
    """Main startup function"""
    logger.info("=" * 60)
    logger.info("Starting AI Interviewer Application")
    logger.info("=" * 60)
    
    # Check Python version
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current directory: {os.getcwd()}")
    logger.info(f"Python path: {sys.path[:3]}")
    
    # Check environment variables
    if not check_environment():
        logger.error("Environment check failed! Continuing anyway...")
    
    # Get port from environment
    port = int(os.getenv('PORT', 8000))
    logger.info(f"PORT environment variable: {port}")
    
    # Check if we can import required modules
    logger.info("Checking critical imports...")
    try:
        import fastapi
        logger.info(f"✓ FastAPI version: {fastapi.__version__}")
        
        import uvicorn
        logger.info(f"✓ Uvicorn version: {uvicorn.__version__}")
        
    except ImportError as e:
        logger.error(f"✗ Critical import error: {e}")
        sys.exit(1)
    
    # Try to import the application
    logger.info("Importing application...")
    try:
        from backend.app.main import app
        logger.info("✓ Application imported successfully")
        
    except Exception as e:
        logger.error(f"✗ Failed to import application: {e}")
        import traceback
        traceback.print_exc()
        logger.error("Attempting to continue anyway...")
    
    # Start the server
    logger.info("=" * 60)
    logger.info(f"Starting Uvicorn server on 0.0.0.0:{port}")
    logger.info("=" * 60)
    
    try:
        import uvicorn
        uvicorn.run(
            "backend.app.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"✗ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
