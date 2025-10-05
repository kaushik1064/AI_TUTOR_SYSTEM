# Pydantic data models
"""
Pydantic models for AI Tutor System
Defines data schemas for validation and serialization
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, EmailStr, validator, Field

# Enums for controlled values
class AcademicLevel(str, Enum):
    elementary = "elementary"
    middle_school = "middle_school" 
    high_school = "high_school"
    undergraduate = "undergraduate"
    graduate = "graduate"

class StudyStyle(str, Enum):
    visual = "visual"
    auditory = "auditory"
    kinesthetic = "kinesthetic"
    mixed = "mixed"

class EmotionState(str, Enum):
    happy = "happy"
    excited = "excited"
    neutral = "neutral"
    confused = "confused"
    stressed = "stressed"
    sad = "sad"
    frustrated = "frustrated"

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class ReminderStatus(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"

class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

# User-related models
class LearningPreferences(BaseModel):
    """Student learning preferences"""
    study_style: StudyStyle = StudyStyle.mixed
    reminder_frequency: str = "daily"
    preferred_study_time: Optional[str] = None
    break_intervals: int = 25  # Pomodoro technique default
    difficulty_preference: str = "adaptive"

class UserBase(BaseModel):
    """Base user model"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    academic_level: AcademicLevel
    subjects: List[str] = Field(default=[], max_items=20)
    learning_preferences: LearningPreferences = LearningPreferences()

class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    """User update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    academic_level: Optional[AcademicLevel] = None
    subjects: Optional[List[str]] = Field(None, max_items=20)
    learning_preferences: Optional[LearningPreferences] = None

class User(UserBase):
    """Complete user model"""
    user_id: str
    created_at: datetime
    last_active: datetime
    total_study_time: int = 0  # in minutes
    conversations_count: int = 0

# Message and Conversation models
class Message(BaseModel):
    """Individual message in conversation"""
    role: MessageRole
    content: str = Field(..., min_length=1, max_length=5000)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    emotion_detected: Optional[EmotionState] = None
    understanding_level: Optional[int] = Field(None, ge=1, le=10)
    study_session_id: Optional[str] = None

class ConversationBase(BaseModel):
    """Base conversation model"""
    user_id: str
    session_type: str = "general"  # general, study_session, check_in
    
class ConversationCreate(ConversationBase):
    """Conversation creation model"""
    initial_message: Optional[str] = None

class Conversation(ConversationBase):
    """Complete conversation model"""
    conversation_id: str
    messages: List[Message] = []
    created_at: datetime
    updated_at: datetime
    session_summary: Optional[str] = None
    topics_discussed: List[str] = []
    total_duration: int = 0  # in minutes
    is_active: bool = True

# Academic Progress models
class AcademicProgressBase(BaseModel):
    """Base academic progress model"""
    user_id: str
    subject: str = Field(..., min_length=1, max_length=100)
    topic: str = Field(..., min_length=1, max_length=200)
    understanding_level: int = Field(..., ge=1, le=10)
    study_date: datetime = Field(default_factory=datetime.utcnow)
    time_spent: int = Field(..., ge=1)  # minutes
    
class AcademicProgressCreate(AcademicProgressBase):
    """Academic progress creation model"""
    notes: Optional[str] = Field(None, max_length=1000)
    difficulty_rating: Optional[int] = Field(None, ge=1, le=5)

class AcademicProgress(AcademicProgressBase):
    """Complete academic progress model"""
    progress_id: str
    feedback_given: Optional[str] = None
    embedding_vector: Optional[List[float]] = None
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

# Reminder models
class ReminderBase(BaseModel):
    """Base reminder model"""
    user_id: str
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    exam_date: datetime
    subject: str = Field(..., min_length=1, max_length=100)
    priority: Priority = Priority.medium

class ReminderCreate(ReminderBase):
    """Reminder creation model"""
    notify_days_before: List[int] = [7, 3, 1]  # Default notification schedule

class ReminderUpdate(BaseModel):
    """Reminder update model"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    exam_date: Optional[datetime] = None
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    priority: Optional[Priority] = None
    status: Optional[ReminderStatus] = None

class Reminder(ReminderBase):
    """Complete reminder model"""
    reminder_id: str
    status: ReminderStatus = ReminderStatus.active
    created_at: datetime
    notifications_sent: List[datetime] = []

# API Response models
class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None

class ChatResponse(BaseModel):
    """Chat API response model"""
    response: str
    emotion_detected: Optional[EmotionState] = None
    understanding_level: Optional[int] = None
    suggestions: List[str] = []
    session_id: Optional[str] = None

# Authentication models
class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    """JWT token payload"""
    user_id: Optional[str] = None
    email: Optional[str] = None

class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr
    password: str
