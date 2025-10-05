"""
AI Tutor System Backend - Working Version (No Firestore)
FastAPI backend with Gemini Pro integration
"""

import logging
import sys
import os
from datetime import datetime, timedelta
from typing import List, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from pydantic import BaseModel

from backend.config import settings
from backend.models import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Tutor System API",
    description="Conversational AI tutor and friend for students (No Firestore)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to load Gemini service
try:
    from services.gemini_service import GeminiService
    gemini_service = GeminiService()
    logger.info("✅ Gemini Pro service loaded")
    GEMINI_AVAILABLE = True
except Exception as e:
    logger.warning(f"⚠️  Gemini service unavailable: {e}")
    GEMINI_AVAILABLE = False

# Security
security = HTTPBearer()

# Mock current user for demo
def get_mock_user():
    return User(
        user_id="demo_user",
        name="Demo Student",
        email="demo@example.com",
        academic_level=AcademicLevel.undergraduate,
        subjects=["Mathematics", "Physics", "Chemistry"],
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow()
    )

# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Tutor System API - Working Version",
        "version": "1.0.0",
        "status": "operational",
        "gemini_available": GEMINI_AVAILABLE,
        "timestamp": datetime.utcnow()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "services": {
            "api": "operational",
            "gemini": "available" if GEMINI_AVAILABLE else "demo_mode",
            "database": "demo_mode"
        }
    }

# Authentication Routes (Demo mode)
@app.post("/api/auth/register", response_model=APIResponse)
async def register_user(user_data: UserCreate):
    """Register new user (Demo mode)"""
    return APIResponse(
        success=True,
        message="User registered successfully (demo mode)",
        data={
            "user_id": f"user_{int(datetime.utcnow().timestamp())}",
            "token": "demo_token_12345",
            "token_type": "bearer"
        }
    )

@app.post("/api/auth/login", response_model=APIResponse)
async def login_user(login_data: LoginRequest):
    """User login (Demo mode)"""
    return APIResponse(
        success=True,
        message="Login successful (demo mode)",
        data={
            "token": "demo_token_12345",
            "token_type": "bearer",
            "expires_in": 3600
        }
    )

# Chat Routes
# In the send_message function, update the emotion values:
@app.post("/api/chat/message", response_model=ChatResponse)
async def send_message(
    message: str,
    conversation_id: Optional[str] = None,
    session_type: str = "general"
):
    """Send message to AI tutor"""
    try:
        import random
        
        # Use valid emotion values that match your model
        valid_emotions = ["happy", "excited", "neutral", "confused", "stressed", "sad", "frustrated"]
        
        # Response templates based on session type
        if session_type == "study_session":
            responses = [
                f"Great! Let's dive into '{message}' for this study session. 📚 How much time do we have today?",
                f"Perfect topic choice: '{message}'. Let's break this down step by step and make sure you really understand it!",
                f"Excellent! I love helping with '{message}'. What specific aspect would you like to focus on first?"
            ]
        elif session_type == "check_in":
            responses = [
                f"Thanks for sharing about '{message}'. How are you feeling about your studies today? 🤗",
                f"I appreciate you mentioning '{message}'. What's been going well for you lately?",
                f"It's great to hear from you about '{message}'. How can I support your learning journey today?"
            ]
        else:
            # For math questions like Pythagorean theorem
            if "pythag" in message.lower() or "theorem" in message.lower():
                responses = [
                    f"Great question about the Pythagorean theorem! 📐 It's one of the most fundamental concepts in geometry. The theorem states that in a right triangle, a² + b² = c², where c is the hypotenuse. Would you like me to explain it with examples?",
                    f"The Pythagorean theorem is fascinating! 🔺 It helps us find missing side lengths in right triangles. For any right triangle, the square of the longest side equals the sum of squares of the other two sides. What specific part would you like to explore?",
                    f"Excellent choice learning about '{message}'! The Pythagorean theorem is used everywhere - from construction to navigation. Let's start with the basic formula: a² + b² = c². Would you like to see some examples?"
                ]
            else:
                responses = [
                    f"That's a fantastic question about '{message}'! 😊 I'd love to help you understand this better. What specific part would you like to explore?",
                    f"Interesting topic: '{message}'! This is something many students find challenging. What's your current understanding?",
                    f"Great question about '{message}'! Let me help break this down for you. Where would you like to start?"
                ]
        
        response_text = random.choice(responses)
        emotion = random.choice(valid_emotions)  # Use valid emotions only
        understanding = random.randint(6, 9)
        
        suggestions = [
            "Take your time to think through the concepts",
            "Practice with similar examples when possible",
            "Don't hesitate to ask follow-up questions",
            "Break complex problems into smaller steps",
            "Review the fundamentals if something feels unclear"
        ]
        
        return ChatResponse(
            response=response_text,
            emotion_detected=emotion,
            understanding_level=understanding,
            suggestions=random.sample(suggestions, 2),
            session_id=conversation_id or f"session_{random.randint(1000, 9999)}"
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return ChatResponse(
            response="I'm having a bit of trouble right now, but I'm still here to help! Could you try asking that again?",
            emotion_detected="neutral",  # Use valid emotion
            session_id=conversation_id
        )


@app.post("/api/chat/session/start", response_model=APIResponse)
async def start_chat_session(session_type: str = "general"):
    """Start new chat session"""
    import random
    session_id = f"session_{random.randint(10000, 99999)}"
    
    return APIResponse(
        success=True,
        message="Chat session started",
        data={"session_id": session_id, "session_type": session_type}
    )

# Academic Progress Routes
@app.get("/api/academic/progress", response_model=List[AcademicProgress])
async def get_progress(days: int = 30):
    """Get user's academic progress"""
    import random
    
    # Generate mock progress data
    mock_progress = []
    subjects = ["Mathematics", "Physics", "Chemistry", "Literature", "History"]
    topics = {
        "Mathematics": ["Calculus Integration", "Linear Algebra", "Statistics", "Differential Equations"],
        "Physics": ["Quantum Mechanics", "Thermodynamics", "Electromagnetism", "Wave Mechanics"],
        "Chemistry": ["Organic Chemistry", "Chemical Bonding", "Reaction Kinetics", "Acid-Base Reactions"],
        "Literature": ["Shakespeare Analysis", "Poetry Interpretation", "Essay Writing", "Literary Devices"],
        "History": ["World War II", "Industrial Revolution", "Ancient Civilizations", "Modern Politics"]
    }
    
    for i in range(10):
        subject = random.choice(subjects)
        topic = random.choice(topics[subject])
        
        progress = AcademicProgress(
            progress_id=f"progress_{i}",
            user_id="demo_user",
            subject=subject,
            topic=topic,
            understanding_level=random.randint(6, 10),
            study_date=datetime.utcnow() - timedelta(days=random.randint(0, days)),
            time_spent=random.randint(30, 120),
            created_at=datetime.utcnow()
        )
        mock_progress.append(progress)
    
    return sorted(mock_progress, key=lambda x: x.study_date, reverse=True)

# Reminder Routes
@app.get("/api/reminders", response_model=List[Reminder])
async def get_reminders():
    """Get upcoming reminders"""
    mock_reminders = [
        Reminder(
            reminder_id="1",
            user_id="demo_user",
            title="Mathematics Final Exam",
            description="Calculus and Linear Algebra final examination",
            exam_date=datetime.utcnow() + timedelta(days=15),
            subject="Mathematics",
            priority=Priority.high,
            status="active",
            created_at=datetime.utcnow()
        ),
        Reminder(
            reminder_id="2",
            user_id="demo_user",
            title="Physics Lab Report Due",
            description="Quantum mechanics laboratory report submission",
            exam_date=datetime.utcnow() + timedelta(days=8),
            subject="Physics",
            priority=Priority.medium,
            status="active",
            created_at=datetime.utcnow()
        ),
        Reminder(
            reminder_id="3",
            user_id="demo_user",
            title="Chemistry Quiz",
            description="Organic chemistry concepts quiz",
            exam_date=datetime.utcnow() + timedelta(days=12),
            subject="Chemistry",
            priority=Priority.high,
            status="active",
            created_at=datetime.utcnow()
        )
    ]
    
    return mock_reminders

@app.post("/api/reminders", response_model=APIResponse)
async def create_reminder(reminder_data: ReminderCreate):
    """Create exam reminder"""
    import random
    
    reminder = Reminder(
        reminder_id=f"reminder_{random.randint(1000, 9999)}",
        user_id="demo_user",
        title=reminder_data.title,
        description=reminder_data.description or "",
        exam_date=reminder_data.exam_date,
        subject=reminder_data.subject,
        priority=reminder_data.priority,
        status="active",
        created_at=datetime.utcnow()
    )
    
    return APIResponse(
        success=True,
        message="Reminder created successfully",
        data=reminder.dict()
    )

# User Profile Routes
@app.get("/api/users/profile", response_model=User)
async def get_user_profile():
    """Get user profile"""
    return get_mock_user()

# Reports Route
@app.get("/api/reports/summary", response_model=APIResponse)
async def get_user_report(days: int = 7):
    """Generate user progress report"""
    mock_report = {
        "user_name": "Demo Student",
        "report_period": {"days": days, "start_date": datetime.utcnow() - timedelta(days=days), "end_date": datetime.utcnow()},
        "study_statistics": {
            "total_study_time": 420,  # 7 hours
            "session_count": 12,
            "average_understanding": 8.2,
            "subjects_studied": ["Mathematics", "Physics", "Chemistry", "Literature"]
        },
        "subject_breakdown": {
            "Mathematics": {"time": 180, "understanding": 8.5, "sessions": 4},
            "Physics": {"time": 120, "understanding": 7.8, "sessions": 3},
            "Chemistry": {"time": 90, "understanding": 8.9, "sessions": 3},
            "Literature": {"time": 30, "understanding": 7.2, "sessions": 2}
        },
        "ai_recommendations": [
            "🎯 Excellent progress in Mathematics! Your understanding has improved significantly.",
            "📚 Consider spending a bit more time on Literature concepts - practice makes perfect!",
            "⏰ Great job maintaining consistent study sessions. Keep up the momentum!",
            "🧠 Your Chemistry performance is outstanding - you're really mastering those concepts!"
        ],
        "achievements": [
            "🔥 Study Streak Champion - 7 consecutive days!",
            "📚 Multi-Subject Learner - Active in 4+ subjects",
            "⭐ High Achiever - Average understanding above 8/10",
            "⏰ Consistent Studier - Regular daily sessions"
        ],
        "upcoming_reminders": 3,
        "study_streaks": {
            "current_streak": 7,
            "longest_streak": 12
        }
    }
    
    return APIResponse(
        success=True,
        message="Report generated successfully",
        data=mock_report
    )

# Additional utility endpoints
@app.get("/api/subjects")
async def get_subjects():
    """Get available subjects"""
    return {
        "subjects": [
            "Mathematics", "Physics", "Chemistry", "Biology",
            "English Literature", "History", "Geography", "Computer Science",
            "Psychology", "Economics", "Art", "Music", "Languages"
        ]
    }

@app.get("/api/stats/quick")
async def get_quick_stats():
    """Get quick statistics for dashboard"""
    import random
    
    return {
        "study_streak": random.randint(5, 15),
        "total_hours_week": random.randint(8, 25),
        "active_subjects": random.randint(3, 6),
        "avg_understanding": round(random.uniform(7.5, 9.2), 1),
        "upcoming_reminders": random.randint(1, 5)
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_no_firestore:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
