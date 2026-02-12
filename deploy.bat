@echo off
echo ========================================
echo   AI Interviewer - Quick Deploy Script
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.12+
    pause
    exit /b 1
)

echo.
echo Installing/Updating dependencies...
python -m pip install --upgrade pip
pip install -r backend\requirements.txt

echo.
echo Setting up database...
python -c "from backend.app.db import init_db; init_db()"

echo.
echo ========================================
echo   Deployment Ready!
echo ========================================
echo.
echo Choose deployment option:
echo.
echo 1. Run locally (http://localhost:8000)
echo 2. Run on network (accessible from other devices)
echo 3. Build Docker image
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting server on localhost:8000...
    echo Press Ctrl+C to stop
    echo.
    uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
)

if "%choice%"=="2" (
    echo.
    echo Finding your local IP address...
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
        set IP=%%a
        goto :found
    )
    :found
    echo.
    echo Starting server on network...
    echo Access from other devices at: http://%IP::=%:8000
    echo Press Ctrl+C to stop
    echo.
    uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
)

if "%choice%"=="3" (
    echo.
    echo Building Docker image...
    docker build -t ai-interviewer .
    echo.
    echo Docker image built successfully!
    echo Run with: docker-compose up -d
    pause
)

if "%choice%"=="4" (
    exit /b 0
)

pause
