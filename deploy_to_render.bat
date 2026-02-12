@echo off
echo ========================================
echo   AI Interviewer - Render Deployment
echo ========================================
echo.

echo This script will help you deploy to Render.com
echo.

echo Step 1: Initialize Git Repository
echo ---------------------------------
git init
if %errorlevel% neq 0 (
    echo Git already initialized
)

echo.
echo Step 2: Add all files to Git
echo ---------------------------------
git add .

echo.
echo Step 3: Create initial commit
echo ---------------------------------
git commit -m "Initial commit - AI Interviewer ready for deployment"

echo.
echo Step 4: Instructions for GitHub
echo ---------------------------------
echo.
echo Now you need to:
echo 1. Create a GitHub repository at https://github.com/new
echo 2. Name it: ai-interviewer
echo 3. Make it PUBLIC (required for Render free tier)
echo 4. DO NOT initialize with README
echo.
echo Then run these commands:
echo.
echo   git remote add origin https://github.com/YOUR_USERNAME/ai-interviewer.git
echo   git branch -M main
echo   git push -u origin main
echo.
echo Replace YOUR_USERNAME with your actual GitHub username
echo.

echo.
echo Step 5: Deploy to Render
echo ---------------------------------
echo.
echo Go to: https://render.com
echo 1. Sign up / Log in
echo 2. Click "New +" -^> "Web Service"
echo 3. Connect your GitHub repository
echo 4. Use these settings:
echo.
echo    Build Command: pip install -r backend/requirements.txt
echo    Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
echo.
echo 5. Add Environment Variables:
echo    GEMINI_API_KEY=AIzaSyB4wAyGTwPKk8coP4Vd7dge9rNXJUq0UqE
echo    SECRET_KEY=EvCF-SmaNGsy8s3K1v2vL9r6RE5R-nQZtehT26vC4Ns
echo    DATABASE_URL=sqlite:///./interview.db
echo    API_V1_STR=/api/v1
echo.
echo 6. Click "Create Web Service"
echo.

echo.
echo ========================================
echo   Deployment Preparation Complete!
echo ========================================
echo.
echo Your project is ready to deploy!
echo.
echo For detailed instructions, see:
echo   render_deployment_guide.md
echo.

pause
