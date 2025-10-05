```markdown
# 🎓 AI Tutor System - Your Personal Learning Companion

An intelligent, conversational AI tutoring system that provides personalized academic support, emotional guidance, and progress tracking for students. Powered by Google's Gemini Pro AI and built with FastAPI and Streamlit.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Gemini Pro](https://img.shields.io/badge/Gemini%20Pro-AI-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Demo Mode vs Production](#-demo-mode-vs-production)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Firebase/Firestore Setup](#-firebasefirestore-setup-optional)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🤖 Conversational AI Tutoring
- Powered by Google Gemini Pro for intelligent, context-aware responses
- Multiple session types: General Chat, Study Sessions, Check-ins, Exam Prep
- Emotion detection and understanding level tracking
- Personalized study tips and recommendations

### 📊 Progress Tracking & Analytics
- Real-time study time tracking
- Subject-wise performance analytics
- Understanding level trends over time
- Interactive charts and visualizations (Plotly)
- Achievement badges and milestones

### 📈 Comprehensive Reports
- Weekly and monthly progress summaries
- Subject deep-dive analysis
- Emotional wellbeing tracking
- AI-generated insights and recommendations
- Export options (PDF, Excel, CSV)

### 📅 Smart Reminders
- Exam and deadline notifications
- Priority-based reminder system
- Study schedule management
- Calendar integration

### 😊 Emotional Support
- Mood tracking and wellbeing monitoring
- Stress level analysis
- Motivational messages
- Mental health recommendations

### 🎯 Study Tools
- Pomodoro timer (25-minute study sessions)
- Quick action shortcuts
- Subject-specific study tips
- Conversation history export

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ Chat UI      │ │ Dashboard    │ │ Reports      │       │
│  │ Components   │ │ Analytics    │ │ Generator    │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ Chat Service │ │ Auth Service │ │ Analytics    │       │
│  │              │ │              │ │ Service      │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  ┌──────────────┐ ┌──────────────┐                         │
│  │ Gemini Pro   │ │ Firebase     │                         │
│  │ (AI Engine)  │ │ (Optional)   │                         │
│  └──────────────┘ └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

**Backend:**
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.8+** - Core programming language
- **Google Gemini Pro** - AI/ML model for conversational intelligence
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server for production deployment

**Frontend:**
- **Streamlit** - Interactive web application framework
- **Plotly** - Interactive data visualization
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP client for API communication

**Optional (Production):**
- **Firebase/Firestore** - Cloud database and authentication
- **Google Cloud** - Hosting and infrastructure

---

## 🔄 Demo Mode vs Production

### 📝 Current Implementation: **Demo Mode**

The application currently runs in **Demo Mode** without Firebase/Firestore. This means:

#### ✅ What Works:
- ✅ Full AI tutoring with Gemini Pro (real AI responses)
- ✅ All UI/UX features and navigation
- ✅ Chat interface with emotion detection
- ✅ Progress visualization and charts
- ✅ Reports generation with analytics
- ✅ Reminder system interface
- ✅ User authentication (demo/mock)

#### ⚠️ Limitations (Demo Mode):
- ⚠️ **No Data Persistence** - All data is stored in-memory (browser session)
  - Chat history lost on page refresh
  - Progress data resets on restart
  - Reminders don't persist across sessions
  
- ⚠️ **No User Differentiation** - Everyone shares the same demo account
  - No individual user profiles
  - No private data separation
  - No real authentication
  
- ⚠️ **Mock Data** - Progress reports use randomly generated data
  - Not based on actual study patterns
  - Resets on every page load
  
- ⚠️ **Single Device** - No cross-device synchronization
  - Can't access history from phone after studying on laptop
  - No cloud backup

#### Why Demo Mode?

We disabled Firebase/Firestore to:
1. Simplify initial setup and testing
2. Allow development without cloud dependencies
3. Enable quick demos and presentations
4. Avoid authentication complexity during development
5. Reduce costs during development phase

---

### 🚀 Production Mode (With Firebase)

To enable full production features with persistent data:

#### ✅ Additional Features with Firebase:
- ✅ **Permanent Data Storage** - All conversations, progress, and user data saved forever
- ✅ **Real User Accounts** - Secure authentication with email/password
- ✅ **Multi-User Support** - Thousands of students with isolated data
- ✅ **Cross-Device Sync** - Access your data from phone, tablet, laptop
- ✅ **Historical Analytics** - Track progress over weeks and months
- ✅ **Scheduled Notifications** - Real exam reminders via email/push
- ✅ **Data Export** - Download your complete study history
- ✅ **Parent/Teacher Dashboard** - Monitor student progress (optional)

#### 📋 See [Firebase/Firestore Setup](#-firebasefirestore-setup-optional) section for instructions

---

## 📦 Prerequisites

Before installation, ensure you have:

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager, included with Python)
- **Git** (for cloning the repository)
- **Google Gemini Pro API Key** ([Get one here](https://ai.google.dev/))
- **Firebase Project** (Optional, for production mode)

---

## 🚀 Installation

### 1. Clone the Repository

```
git clone https://github.com/yourusername/ai-tutor-system.git
cd ai-tutor-system
```

### 2. Create Virtual Environment

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

**Required packages:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
streamlit==1.28.1
pydantic==2.4.2
pydantic-settings==2.0.3
python-dotenv==1.0.0
requests==2.31.0
pandas==2.1.3
plotly==5.18.0
google-generativeai==0.3.1
email-validator==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Optional (for production with Firebase)
firebase-admin==6.2.0
google-cloud-firestore==2.13.1
```

---

## ⚙️ Configuration

### 1. Create Environment File

Create a `.env` file in the project root:

```
# Copy the example file
cp .env.example .env

# Or create manually
touch .env
```

### 2. Configure Environment Variables

**Minimum configuration (Demo Mode):**

```
# Google Gemini Pro API
GEMINI_API_KEY=your_gemini_api_key_here

# Google Cloud (for Gemini Pro)
GOOGLE_CLOUD_PROJECT=your-project-id

# Security (generate a secure random key)
SECRET_KEY=your-secret-key-here-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=True
HOST=0.0.0.0
PORT=8000

# AI Configuration
MAX_CONVERSATION_LENGTH=50
EMBEDDING_DIMENSION=768
TEMPERATURE=0.7
MAX_TOKENS=1000
```

### 3. Get Your Gemini Pro API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Create a new API key for your project
4. Copy the key and paste it in your `.env` file

### 4. Generate Secret Key

```
# Run this in Python to generate a secure secret key
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🎮 Running the Application

### Method 1: Quick Start (Recommended)

**Terminal 1 - Start Backend:**
```
cd backend
python main_no_firestore.py
```

You should see:
```
INFO: Uvicorn running on http://0.0.0.0:8000
✅ Gemini Pro service initialized successfully
INFO: Application startup complete.
```

**Terminal 2 - Start Frontend:**
```
cd frontend
streamlit run app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Method 2: Using Uvicorn Directly

**Backend:**
```
cd backend
uvicorn main_no_firestore:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```
streamlit run frontend/app.py --server.port 8501
```

### Access the Application

- **Frontend (Main UI)**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
ai_tutor_system/
│
├── backend/                      # FastAPI backend
│   ├── main.py                   # Main backend (with Firebase)
│   ├── main_no_firestore.py      # Demo backend (no Firebase) ⭐
│   ├── config.py                 # Configuration and settings
│   ├── models.py                 # Pydantic data models
│   ├── auth.py                   # Authentication logic
│   ├── analytics.py              # Analytics service
│   └── chat_service.py           # Chat processing logic
│
├── frontend/                     # Streamlit frontend
│   ├── app.py                    # Main Streamlit application
│   └── components/               # UI components
│       ├── __init__.py
│       ├── chat_interface.py     # Chat UI component
│       ├── dashboard.py          # Analytics dashboard
│       └── reports.py            # Reports generator
│
├── services/                     # External service integrations
│   ├── gemini_service.py         # Gemini Pro AI integration
│   └── firestore_service.py      # Firebase/Firestore (optional)
│
├── utils/                        # Utility functions
│   └── helpers.py                # Helper functions
│
├── .env                          # Environment variables (create this)
├── .env.example                  # Example environment file
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                     # This file
```

### Key Files

- **`main_no_firestore.py`** ⭐ - Current backend implementation (Demo Mode)
- **`main.py`** - Full backend with Firebase (for production)
- **`app.py`** - Streamlit frontend entry point
- **`gemini_service.py`** - Gemini Pro AI integration
- **`config.py`** - All configuration settings

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Main Endpoints

#### Health Check
```
GET /health
```
**Response:**
```
{
  "status": "healthy",
  "timestamp": "2025-10-05T16:13:00",
  "services": {
    "api": "operational",
    "gemini": "available",
    "database": "demo_mode"
  }
}
```

#### Chat with AI Tutor
```
POST /api/chat/message
```
**Parameters:**
- `message` (string, required) - User's question or message
- `session_type` (string, optional) - Type of session: `general`, `study_session`, `check_in`, `exam_prep`
- `conversation_id` (string, optional) - Continue existing conversation

**Response:**
```
{
  "response": "Great question about the Pythagorean theorem! 📐 ...",
  "emotion_detected": "excited",
  "understanding_level": 8,
  "suggestions": [
    "Practice with similar examples",
    "Draw diagrams to visualize"
  ],
  "session_id": "session_1234"
}
```

#### Get Academic Progress
```
GET /api/academic/progress?days=30
```
**Response:**
```
[
  {
    "progress_id": "progress_1",
    "user_id": "demo_user",
    "subject": "Mathematics",
    "topic": "Calculus Integration",
    "understanding_level": 8,
    "study_date": "2025-10-05T10:30:00",
    "time_spent": 90
  }
]
```

#### Get Reminders
```
GET /api/reminders
```

#### Generate Progress Report
```
GET /api/reports/summary?days=7
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI with:
- Try out all endpoints
- See request/response schemas
- Test authentication
- Example requests and responses

---

## 🔥 Firebase/Firestore Setup (Optional)

To enable production mode with persistent data storage:

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. Follow the setup wizard
4. Enable Firestore Database

### 2. Generate Service Account Key

1. In Firebase Console, go to **Project Settings** → **Service Accounts**
2. Click "Generate New Private Key"
3. Save the JSON file as `firebase-credentials.json` in your project root
4. **⚠️ NEVER commit this file to Git!**

### 3. Configure Environment Variables

Add to your `.env` file:

```
# Firebase Configuration
GOOGLE_APPLICATION_CREDENTIALS=./firebase-credentials.json

# Firebase JSON Config (single line)
FIREBASE_CONFIG={"type":"service_account","project_id":"your-project-id",...}
```

### 4. Update Backend to Use Firebase

**Switch from `main_no_firestore.py` to `main.py`:**

```
# Uncomment Firebase imports in main.py
from services.firestore_service import firestore_service
from backend.analytics import analytics_service

# Run the full backend
python backend/main.py
```

### 5. Initialize Firestore Collections

The application will automatically create these collections:
- `users` - User accounts and profiles
- `conversations` - Chat history
- `academic_progress` - Study sessions and progress
- `reminders` - Exam reminders and deadlines

### 6. Test Firebase Connection

```
# Test script
python -c "
from services.firestore_service import firestore_service
print('Firebase initialized:', firestore_service.db is not None)
"
```

---

## 📸 Screenshots

### Chat Interface
```
┌─────────────────────────────────────────────┐
│  💬 Chat with Your AI Tutor                │
│  ┌────────────────────────────────────┐    │
│  │ User: What is the Pythagorean     │    │
│  │       theorem?                     │    │
│  └────────────────────────────────────┘    │
│  ┌────────────────────────────────────┐    │
│  │ AI: Great question! The Pythagorean│    │
│  │     theorem states that in a right │    │
│  │     triangle, a² + b² = c²...      │    │
│  │     😊 Emotion: excited             │    │
│  │     📊 Understanding: 8/10          │    │
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### Dashboard Analytics
```
┌─────────────────────────────────────────────┐
│  📊 Your Learning Dashboard                │
│  ┌────┬────┬────┬────┐                     │
│  │📅 7│⏰18h│📚 4│🎯8.2│                    │
│  └────┴────┴────┴────┘                     │
│  [Study Progress Chart]                     │
│  [Subject Distribution Pie]                 │
└─────────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Gemini API Error
```
Error: 403 Permission denied
```
**Solution:**
- Check your `GEMINI_API_KEY` in `.env`
- Ensure API key is valid and active
- Check API quota/billing in Google Cloud Console

#### 2. Module Not Found Error
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:**
```
pip install -r requirements.txt
# Or install individually
pip install streamlit plotly pandas
```

#### 3. Port Already in Use
```
Error: Address already in use
```
**Solution:**
```
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### 4. Streamlit Widget Duplicate Key Error
```
DuplicateWidgetID: Multiple identical st.button widgets
```
**Solution:**
- Each widget needs a unique `key` parameter
- Add: `st.button("Text", key="unique_key_name")`

#### 5. Firebase Authentication Error (If using Firebase)
```
DefaultCredentialsError: Credentials not found
```
**Solution:**
```
set GOOGLE_APPLICATION_CREDENTIALS=path\to\firebase-credentials.json
```

### Debug Mode

Enable detailed logging:

```
# In config.py
DEBUG=True

# Run with verbose logging
uvicorn main_no_firestore:app --log-level debug
```

### Need Help?

- Check [Issues](https://github.com/yourusername/ai-tutor-system/issues) on GitHub
- Read the [FastAPI Docs](https://fastapi.tiangolo.com/)
- Read the [Streamlit Docs](https://docs.streamlit.io/)
- Contact: your.email@example.com

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### 1. Fork the Repository

```
git clone https://github.com/yourusername/ai-tutor-system.git
cd ai-tutor-system
```

### 2. Create a Feature Branch

```
git checkout -b feature/amazing-feature
```

### 3. Make Your Changes

- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation as needed
- Test your changes thoroughly

### 4. Commit Your Changes

```
git add .
git commit -m "Add amazing feature"
```

### 5. Push and Create Pull Request

```
git push origin feature/amazing-feature
```

### Development Guidelines

- Write clear, descriptive commit messages
- Update README.md if adding new features
- Add unit tests for new functionality
- Ensure all tests pass before submitting PR
- Keep PRs focused on a single feature/fix

---


