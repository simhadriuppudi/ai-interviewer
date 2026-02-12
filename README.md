# Voice-Enabled AI Interviewer

A complete end-to-end web application that conducts personalized voice-based interviews using **Google Gemini AI** and **RAG** (Retrieval-Augmented Generation).

## 🚀 Features

- **Voice-Enabled Interviews**: Real-time Speech-to-Text (STT) and Text-to-Speech (TTS) using Web Speech API
- **RAG Intelligence**: Parses your Resume (PDF/DOCX) and Job Description to generate relevant questions
- **Gemini AI**: Powered by Google's `gemini-3-flash-preview` model for intelligent question generation and evaluation
- **Multi-Interview Types**: Support for HR, Technical, and Aptitude interviews
- **Performance Analytics**: Detailed feedback reports with scoring on accuracy, clarity, and confidence
- **Historical Comparison**: Track improvement across multiple interview attempts
- **PDF Reports**: Downloadable interview performance reports
- **Modern UI**: Glassmorphism design with dark theme, responsive, and animated

## 🛠️ Prerequisites

1. **Python 3.10+**
2. **Google Gemini API Key**: Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Modern Web Browser**: Chrome or Edge (for Web Speech API support)

## 📦 Setup Instructions

### 1. Clone/Download the Repository

Download or clone this repository to your local machine.

### 2. Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
SECRET_KEY=your_secret_jwt_key_change_this
```

### 3. Install Dependencies

#### Windows:

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

#### Linux/Mac:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 4. Initialize Database

The database will be automatically created when you first run the application.

## ▶️ Running the Application

### Start the Backend Server

```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Run the server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### Access the Application

Open your web browser and navigate to:

**http://localhost:8000**

The frontend is served as static files by the FastAPI backend.

## 🧪 How to Use

### 1. Register/Login

- Create a new account with your email and password
- Or login if you already have an account

### 2. Setup Interview

- **Upload Resume**: Upload your resume (PDF or DOCX format)
- **Paste Job Description**: Copy and paste the job description
- **Select Interview Types**: Choose one or more interview types:
  - HR Interview
  - Technical Interview
  - Aptitude Interview
- Click **Start Interview**

### 3. Voice Interview

- The AI will ask you questions based on your resume and job description
- Click the **microphone button** to speak your answer
- The AI will listen, process your response, and ask follow-up questions
- Speak clearly and at a moderate pace
- Continue until you've answered all questions or click **End Interview**

### 4. View Performance Report

- After ending the interview, you'll see a detailed performance report
- Metrics include:
  - Overall Score (0-100)
  - Accuracy Score (0-10)
  - Clarity Score (0-10)
  - Confidence Score (0-10)
- View your strengths, weaknesses, and actionable improvement suggestions
- If you've taken previous interviews, see how you've improved
- Download the report as PDF

### 5. Take More Interviews

- Click **Take Another Interview** to practice more
- Each interview is saved to your history
- Track your progress over time

## 🏗️ Architecture

### Backend (FastAPI)

- **Authentication**: JWT-based user authentication
- **Database**: SQLite with SQLModel ORM
- **RAG Engine**: FAISS vector store with SentenceTransformers embeddings
- **AI**: Google Gemini API for question generation and analysis
- **Voice**: gTTS for Text-to-Speech conversion

### Frontend (HTML/CSS/JS)

- **UI**: Modern glassmorphism design with dark theme
- **Voice**: Web Speech API for Speech-to-Text
- **Styling**: Vanilla CSS with animations
- **No Framework**: Pure JavaScript for maximum compatibility

### Key Components

- `backend/app/services/gemini_service.py`: Gemini AI integration
- `backend/app/services/voice_service.py`: Text-to-Speech service
- `backend/app/services/rag.py`: RAG engine for context retrieval
- `backend/app/api/interview.py`: Interview flow API
- `backend/app/api/analytics.py`: Performance analytics API
- `frontend/interview.html`: Voice-enabled interview interface
- `frontend/js/interview.js`: Voice interaction logic

## 📁 Project Structure

```
aiInterviewer-4/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration
│   │   ├── models/       # Database models
│   │   └── services/     # Business logic (Gemini, RAG, Voice)
│   └── requirements.txt
├── frontend/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   ├── index.html        # Landing page
│   ├── login.html        # Authentication
│   ├── dashboard.html    # Interview setup
│   ├── interview.html    # Voice interview
│   └── report.html       # Performance report
├── uploads/              # Uploaded resumes
├── vector_store/         # FAISS vector database
├── interview.db          # SQLite database
├── .env.example          # Environment template
└── README.md
```

## 🔧 Configuration

All configuration is in `.env` file:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `SECRET_KEY`: JWT secret key for authentication
- `DATABASE_URL`: SQLite database path
- `MAX_QUESTIONS_PER_INTERVIEW`: Maximum questions per session (default: 10)

## 🐛 Troubleshooting

### Speech Recognition Not Working

- **Solution**: Use Chrome or Edge browser. Safari and Firefox have limited support.
- Ensure you're using HTTPS or localhost (required for microphone access)
- Grant microphone permissions when prompted

### Gemini API Errors

- **Solution**: Check that your API key is correct in `.env`
- Verify you have API quota remaining
- Check your internet connection

### Database Errors

- **Solution**: Delete `interview.db` and restart the server to recreate it

### Voice Not Playing

- **Solution**: Check browser audio permissions
- Ensure speakers/headphones are connected
- Try refreshing the page

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Change the `SECRET_KEY` in production
- Use HTTPS in production for secure microphone access
- Passwords are hashed with bcrypt

## 📝 API Documentation

Once the server is running, visit:

**http://localhost:8000/docs**

For interactive API documentation (Swagger UI).

## 🎯 Future Enhancements

- Video interview support
- Multi-language support
- Advanced analytics dashboard
- Interview scheduling
- Team collaboration features
- Mobile app

## 📄 License

This project is for educational and personal use.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Support

For issues or questions, please open an issue on the repository.

---

**Built with ❤️ using FastAPI, Gemini AI, and Modern Web Technologies**
