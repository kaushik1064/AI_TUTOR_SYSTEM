# 🎓 AI Tutor System — Your Personal Learning Companion

An intelligent, conversational AI tutoring system that provides personalized academic support, emotional guidance, and progress tracking for students. Powered by Google's Gemini Pro AI and built with FastAPI and Streamlit.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Gemini Pro](https://img.shields.io/badge/Gemini%20Pro-AI-purple)


---

## Table of contents

- [Features](#features)
- [Architecture](#architecture)
- [Demo Mode vs Production](#demo-mode-vs-production)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the application](#running-the-application)
- [Project structure](#project-structure)
- [API documentation](#api-documentation)
- [Firebase / Firestore setup (optional)](#firebasefirestore-setup-optional)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Conversational AI Tutoring
- Powered by Google Gemini Pro for intelligent, context-aware responses
- Session types: general chat, study sessions, check-ins, exam prep
- Emotion detection and understanding-level tracking
- Personalized study tips and recommendations

### Progress Tracking & Analytics
- Real-time study time tracking
- Subject-wise performance analytics
- Understanding level trends over time
- Interactive charts and visualizations (Plotly)
- Achievement badges and milestones

### Reports
- Weekly and monthly progress summaries
- Subject deep-dive analysis
- Emotional wellbeing tracking
- AI-generated insights and recommendations
- Export options (PDF, Excel, CSV)

### Smart Reminders
- Exam and deadline notifications
- Priority-based reminder system
- Study schedule management
- Calendar integration

### Emotional Support
- Mood tracking and wellbeing monitoring
- Stress level analysis
- Motivational messages and mental health recommendations

### Study Tools
- Pomodoro timer (25-minute sessions)
- Quick action shortcuts
- Subject-specific study tips
- Conversation history export

---

## Architecture

Frontend (Streamlit)
- Chat UI components
- Dashboard analytics
- Reports generator

Backend (FastAPI)
- Chat service
- Auth service
- Analytics service

External services
- Gemini Pro (AI engine)
- Firebase / Firestore (optional)

Tech stack highlights:
- Backend: FastAPI, Uvicorn, Pydantic
- Frontend: Streamlit, Plotly, Pandas
- AI: Google Gemini Pro
- Optional: Firebase / Firestore

---

## Demo Mode vs Production

### Demo Mode (current)
- Runs without Firebase/Firestore
- Works: AI tutoring, UI features, emotion detection, analytics (mock)
- Limitations:
  - No persistent storage (in-memory only)
  - No per-user accounts or cross-device sync
  - Mocked/random progress data

### Production (with Firebase)
- Persistent storage and real user accounts
- Cross-device sync, scheduled notifications, historical analytics
- Parent/teacher dashboards (optional)

---

## Prerequisites

- Python 3.8+
- pip
- Git
- Google Gemini Pro API key (for AI)
- Firebase project (optional, for production mode)

---

## Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/ai-tutor-system.git
   cd ai-tutor-system
   ```

2. Create a virtual environment

Windows:
```
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

Sample required packages (see requirements.txt for exact pins):
- fastapi, uvicorn[standard], streamlit, pydantic, google-generativeai, pandas, plotly, requests

Optional (Firebase/Firestore):
- firebase-admin, google-cloud-firestore

---

## Configuration

Create a `.env` file in the project root (copy `.env.example` if present).

Minimum variables (Demo Mode):
```
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_CLOUD_PROJECT=your-project-id
SECRET_KEY=your-secret-key-here-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
HOST=0.0.0.0
PORT=8000
MAX_CONVERSATION_LENGTH=50
EMBEDDING_DIMENSION=768
TEMPERATURE=0.7
MAX_TOKENS=1000
```

Generate a secure SECRET_KEY:
```
python - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
```

---

## Running the application

Recommended quick start (Demo backend + Streamlit frontend)

Terminal 1 — Backend:
```
cd backend
python main_no_firestore.py
```

Terminal 2 — Frontend:
```
cd frontend
streamlit run app.py
```

Access:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Alternative using uvicorn:
```
cd backend
uvicorn main_no_firestore:app --reload --host 0.0.0.0 --port 8000
```
Streamlit with explicit port:
```
streamlit run frontend/app.py --server.port 8501
```

---

## Project structure

```
ai_tutor_system/
├── backend/
│   ├── main.py
│   ├── main_no_firestore.py    # Demo backend (no Firebase)
│   ├── config.py
│   ├── models.py
│   ├── auth.py
│   ├── analytics.py
│   └── chat_service.py
├── frontend/
│   ├── app.py
│   └── components/
│       ├── chat_interface.py
│       ├── dashboard.py
│       └── reports.py
├── services/
│   ├── gemini_service.py
│   └── firestore_service.py
├── utils/
│   └── helpers.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

Key files:
- backend/main_no_firestore.py — demo backend
- backend/main.py — production backend (with Firebase)
- frontend/app.py — Streamlit app
- services/gemini_service.py — Gemini Pro integration
- backend/config.py — configuration and settings

---

## API Documentation (selected endpoints)

Base URL: `http://localhost:8000`

Health:
```
GET /health
```
Sample response:
```json
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

Chat:
```
POST /api/chat/message
```
Parameters:
- message (string, required)
- session_type (string, optional) — e.g., general, study_session, exam_prep
- conversation_id (string, optional)

Sample response:
```json
{
  "response": "Great question about the Pythagorean theorem! 📐 ...",
  "emotion_detected": "excited",
  "understanding_level": 8,
  "suggestions": ["Practice with similar examples", "Draw diagrams to visualize"],
  "session_id": "session_1234"
}
```

Progress:
```
GET /api/academic/progress?days=30
```

Reminders:
```
GET /api/reminders
```

Reports:
```
GET /api/reports/summary?days=7
```

Visit `/docs` for Swagger UI to try endpoints interactively.

---

## Firebase / Firestore setup (optional)

1. Create a Firebase project and enable Firestore.
2. Generate a service account JSON key and save it as `firebase-credentials.json` (DO NOT commit).
3. Set environment variable:
```
set GOOGLE_APPLICATION_CREDENTIALS=.\firebase-credentials.json
```
4. Add to `.env` if needed:
```
FIREBASE_CONFIG={"type":"service_account","project_id":"your-project-id",...}
```
5. Switch to production backend:
```
cd backend
python main.py
```
Test Firebase connection:
```
python -c "from services.firestore_service import firestore_service; print('Firebase initialized:', firestore_service.db is not None)"
```

---

## Screenshots (examples)

Chat interface, dashboard analytics and progress charts are implemented in the frontend. See `frontend/components/` for UI components.

---

## Troubleshooting

Common issues and fixes:

- Gemini API 403:
  - Verify `GEMINI_API_KEY` and Google Cloud billing/quotas.

- ModuleNotFoundError (e.g., streamlit):
```
pip install -r requirements.txt
```

- Port in use (Windows):
```
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

- Duplicate Streamlit widget keys:
  - Ensure each widget has a unique `key` parameter.

- Firebase DefaultCredentialsError:
```
set GOOGLE_APPLICATION_CREDENTIALS=path\to\firebase-credentials.json
```

Enable debug logging in config and run uvicorn with `--log-level debug` for more details.

---

## Contributing

1. Fork and clone the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Implement changes, follow PEP8 and document behavior
4. Add tests for new features
5. Commit and push:
```
git add .
git commit -m "Add feature"
git push origin feature/your-feature
```
6. Open a pull request

---


