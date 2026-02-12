@echo off
echo ================================================
echo   Voice-Enabled AI Interviewer - Setup Script
echo ================================================
echo.

REM Check if .env file exists
if not exist .env (
    echo [INFO] Creating .env file from template...
    copy .env.example .env
    echo.
    echo [IMPORTANT] Please edit the .env file and add your Gemini API key!
    echo You can get an API key from: https://makersuite.google.com/app/apikey
    echo.
    pause
)

REM Check if venv exists
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        echo Please ensure Python 3.10+ is installed
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

echo.
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [INFO] Installing dependencies...
pip install -r backend\requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Setup complete!
echo.
echo ================================================
echo   Next Steps:
echo ================================================
echo 1. Edit .env file and add your GEMINI_API_KEY
echo 2. Run: venv\Scripts\activate
echo 3. Run: uvicorn backend.app.main:app --reload
echo 4. Open: http://localhost:8000
echo ================================================
echo.
pause
