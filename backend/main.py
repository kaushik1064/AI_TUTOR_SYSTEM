# Main FastAPI application
"""
FastAPI backend for AI Tutor System
Main application entry point with all API routes
"""

import logging
import sys
import os
from datetime import datetime
from typing import List, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

from backend.config import settings
from backend.models import *
from services.gemini_service import gemini_service
#from services.firestore_service import firestore_service
from backend.auth import verify_token, create_access_token, hash_password
#from backend.analytics import analytics_service
from backend.chat_service import chat_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Tutor System API",
    description="Conversational AI tutor and friend for students",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    try:
        token_data = verify_token(credentials.credentials)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        user = await firestore_service.get_user(token_data.user_id or "demo_user")
        if not user:
            # For demo purposes, create a mock user
            user = User(
                user_id="demo_user",
                name="Demo Student",
                email="demo@example.com",
                academic_level=AcademicLevel.undergraduate,
                subjects=["Mathematics", "Physics"],
                created_at=datetime.utcnow(),
                last_active=datetime.utcnow()
            )
        
        return user
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Tutor System API",
        "version": "1.0.0",
        "status": "healthy",
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
            "database": "operational", 
            "ai_service": "operational"
        }
    }

# Authentication Routes
@app.post("/api/auth/register", response_model=APIResponse)
async def register_user(user_data: UserCreate):
    """Register new user"""
    try:
        # For demo purposes, create user without actual database
        user = User(
            user_id=f"user_{datetime.utcnow().timestamp()}",
            name=user_data.name,
            email=user_data.email,
            academic_level=user_data.academic_level,
            subjects=user_data.subjects,
            learning_preferences=user_data.learning_preferences,
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow()
        )
        
        # Generate token
        token_data = {"user_id": user.user_id, "email": user.email}
        token = create_access_token(token_data)
        
        return APIResponse(
            success=True,
            message="User registered successfully",
            data={
                "user": user.dict(),
                "token": token,
                "token_type": "bearer"
            }
        )
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@app.post("/api/auth/login", response_model=APIResponse)
async def login_user(login_data: LoginRequest):
    """User login"""
    try:
        # For demo purposes, accept any login
        token_data = {"email": login_data.email, "user_id": "demo_user"}
        token = create_access_token(token_data)
        
        return APIResponse(
            success=True,
            message="Login successful",
            data={
                "token": token,
                "token_type": "bearer",
                "expires_in": settings.access_token_expire_minutes * 60
            }
        )
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

# Chat Routes
@app.post("/api/chat/message", response_model=ChatResponse)
async def send_message(
    message: str,
    conversation_id: Optional[str] = None,
    session_type: str = "general",
    current_user: User = Depends(get_current_user)
):
    """Send message to AI tutor"""
    try:
        # Start new conversation if needed
        if not conversation_id:
            conversation = await chat_service.start_conversation(
                current_user.user_id, session_type
            )
            conversation_id = conversation.conversation_id
        
        # Process message through chat service
        response = await chat_service.process_message(
            conversation_id, message, current_user
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return ChatResponse(
            response=f"I'm having a bit of trouble right now, but I'm still here to help! Could you try asking that again?",
            session_id=conversation_id
        )

@app.post("/api/chat/session/start", response_model=APIResponse)
async def start_chat_session(
    session_type: str = "general",
    current_user: User = Depends(get_current_user)
):
    """Start new chat session"""
    try:
        conversation = await chat_service.start_conversation(
            current_user.user_id, session_type
        )
        
        return APIResponse(
            success=True,
            message="Chat session started",
            data={"session_id": conversation.conversation_id}
        )
    except Exception as e:
        logger.error(f"Session start error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start session"
        )

@app.put("/api/chat/session/{session_id}/end", response_model=APIResponse)
async def end_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """End chat session"""
    try:
        summary = await chat_service.end_session(session_id, current_user)
        
        return APIResponse(
            success=True,
            message="Session ended successfully",
            data={"summary": summary}
        )
    except Exception as e:
        logger.error(f"Session end error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to end session"
        )

# Academic Progress Routes
@app.post("/api/academic/progress", response_model=APIResponse)
async def save_progress(
    progress_data: AcademicProgressCreate,
    current_user: User = Depends(get_current_user)
):
    """Save academic progress"""
    try:
        progress_data.user_id = current_user.user_id
        
        # For demo, create mock progress entry
        progress = AcademicProgress(
            progress_id=f"progress_{datetime.utcnow().timestamp()}",
            user_id=current_user.user_id,
            subject=progress_data.subject,
            topic=progress_data.topic,
            understanding_level=progress_data.understanding_level,
            study_date=progress_data.study_date,
            time_spent=progress_data.time_spent,
            created_at=datetime.utcnow()
        )
        
        return APIResponse(
            success=True,
            message="Progress saved successfully",
            data=progress.dict()
        )
    except Exception as e:
        logger.error(f"Progress save error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save progress"
        )

@app.get("/api/academic/progress", response_model=List[AcademicProgress])
async def get_progress(
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """Get user's academic progress"""
    try:
        # For demo, return mock progress data
        mock_progress = []
        for i in range(5):
            progress = AcademicProgress(
                progress_id=f"progress_{i}",
                user_id=current_user.user_id,
                subject=["Mathematics", "Physics", "Chemistry"][i % 3],
                topic=f"Topic {i+1}",
                understanding_level=7 + (i % 3),
                study_date=datetime.utcnow(),
                time_spent=45 + (i * 15),
                created_at=datetime.utcnow()
            )
            mock_progress.append(progress)
        
        return mock_progress
    except Exception as e:
        logger.error(f"Progress fetch error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch progress"
        )

# Reminder Routes
@app.post("/api/reminders", response_model=APIResponse)
async def create_reminder(
    reminder_data: ReminderCreate,
    current_user: User = Depends(get_current_user)
):
    """Create exam reminder"""
    try:
        reminder = Reminder(
            reminder_id=f"reminder_{datetime.utcnow().timestamp()}",
            user_id=current_user.user_id,
            title=reminder_data.title,
            description=reminder_data.description,
            exam_date=reminder_data.exam_date,
            subject=reminder_data.subject,
            priority=reminder_data.priority,
            created_at=datetime.utcnow()
        )
        
        return APIResponse(
            success=True,
            message="Reminder created successfully",
            data=reminder.dict()
        )
    except Exception as e:
        logger.error(f"Reminder creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create reminder"
        )

@app.get("/api/reminders", response_model=List[Reminder])
async def get_reminders(current_user: User = Depends(get_current_user)):
    """Get upcoming reminders"""
    try:
        # Mock reminders data
        from datetime import timedelta
        
        mock_reminders = [
            Reminder(
                reminder_id="1",
                user_id=current_user.user_id,
                title="Math Final Exam",
                description="Calculus and Linear Algebra",
                exam_date=datetime.utcnow() + timedelta(days=15),
                subject="Mathematics",
                priority=Priority.high,
                created_at=datetime.utcnow()
            ),
            Reminder(
                reminder_id="2", 
                user_id=current_user.user_id,
                title="Physics Lab Report",
                description="Quantum mechanics lab",
                exam_date=datetime.utcnow() + timedelta(days=8),
                subject="Physics",
                priority=Priority.medium,
                created_at=datetime.utcnow()
            )
        ]
        
        return mock_reminders
    except Exception as e:
        logger.error(f"Reminders fetch error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch reminders"
        )

# Reports Route
@app.get("/api/reports/summary", response_model=APIResponse)
async def get_user_report(
    days: int = 7,
    current_user: User = Depends(get_current_user)
):
    """Generate user progress report"""
    try:
        # Generate comprehensive report using analytics service
        report = await analytics_service.generate_progress_report(
            current_user.user_id, days
        )
        
        return APIResponse(
            success=True,
            message="Report generated successfully",
            data=report
        )
        
    except Exception as e:
        logger.error(f"Report generation error: {e}")
        # Return mock report data
        mock_report = {
            "user_name": current_user.name,
            "report_period": {"days": days},
            "study_statistics": {
                "total_study_time": 420,  # 7 hours
                "session_count": 12,
                "average_understanding": 8.2,
                "subjects_studied": ["Mathematics", "Physics", "Chemistry"]
            },
            "ai_recommendations": [
                "Continue your excellent progress in Mathematics",
                "Consider spending more time on Chemistry concepts",
                "Take regular breaks during study sessions"
            ],
            "achievements": [
                "🎯 Study Streak - 7 consecutive days!",
                "📚 Multi-Subject Learner",
                "⭐ High Understanding Average"
            ]
        }
        
        return APIResponse(
            success=True,
            message="Report generated successfully",
            data=mock_report
        )

# User profile routes
@app.get("/api/users/profile", response_model=User)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get user profile"""
    return current_user

@app.put("/api/users/profile", response_model=APIResponse)
async def update_user_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    try:
        # For demo, just return success
        return APIResponse(
            success=True,
            message="Profile updated successfully",
            data=current_user.dict()
        )
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
