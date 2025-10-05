# Google Firestore database
"""
Google Firestore database service
Handles user data, conversations, academic progress, and reminders
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import AsyncClient
from google.cloud.firestore_v1.base_query import FieldFilter

from backend.config import settings
from backend.models import *

logger = logging.getLogger(__name__)

class FirestoreService:
    """Firestore database operations service"""
    
    def __init__(self):
        """Initialize Firestore connection"""
        try:
            # Initialize Firebase Admin SDK
            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.get_firebase_config())
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.AsyncClient()
            logger.info("✅ Firestore service initialized")
        except Exception as e:
            logger.error(f"❌ Firestore initialization failed: {e}")
            raise

    # User Management
    async def create_user(self, user_data: UserCreate) -> User:
        """Create new user in Firestore"""
        user_id = str(uuid.uuid4())
        user = User(
            user_id=user_id,
            name=user_data.name,
            email=user_data.email,
            academic_level=user_data.academic_level,
            subjects=user_data.subjects,
            learning_preferences=user_data.learning_preferences,
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow()
        )
        
        await self.db.collection('users').document(user_id).set(user.dict())
        return user

    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        doc = await self.db.collection('users').document(user_id).get()
        if doc.exists:
            return User(**doc.to_dict())
        return None

    async def update_user_activity(self, user_id: str):
        """Update user last active timestamp"""
        await self.db.collection('users').document(user_id).update({
            'last_active': datetime.utcnow()
        })

    # Conversation Management  
    async def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        """Create new conversation"""
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            conversation_id=conversation_id,
            user_id=conversation_data.user_id,
            session_type=conversation_data.session_type,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        await self.db.collection('conversations').document(conversation_id).set(conversation.dict())
        return conversation

    async def add_message(self, conversation_id: str, message: Message):
        """Add message to conversation"""
        await self.db.collection('conversations').document(conversation_id).update({
            'messages': firestore.ArrayUnion([message.dict()]),
            'updated_at': datetime.utcnow()
        })

    async def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Conversation]:
        """Get recent conversations for user"""
        query = self.db.collection('conversations')\
            .where(filter=FieldFilter('user_id', '==', user_id))\
            .order_by('updated_at', direction=firestore.Query.DESCENDING)\
            .limit(limit)
        
        docs = await query.get()
        return [Conversation(**doc.to_dict()) for doc in docs]

    # Academic Progress
    async def save_academic_progress(self, progress_data: AcademicProgressCreate) -> AcademicProgress:
        """Save academic progress entry"""
        progress_id = str(uuid.uuid4())
        progress = AcademicProgress(
            progress_id=progress_id,
            user_id=progress_data.user_id,
            subject=progress_data.subject,
            topic=progress_data.topic,
            understanding_level=progress_data.understanding_level,
            study_date=progress_data.study_date,
            time_spent=progress_data.time_spent,
            created_at=datetime.utcnow()
        )
        
        await self.db.collection('academic_progress').document(progress_id).set(progress.dict())
        return progress

    async def get_user_progress(self, user_id: str, days: int = 30) -> List[AcademicProgress]:
        """Get user's academic progress for specified days"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = self.db.collection('academic_progress')\
            .where(filter=FieldFilter('user_id', '==', user_id))\
            .where(filter=FieldFilter('study_date', '>=', start_date))\
            .order_by('study_date', direction=firestore.Query.DESCENDING)
        
        docs = await query.get()
        return [AcademicProgress(**doc.to_dict()) for doc in docs]

    # Reminders
    async def create_reminder(self, reminder_data: ReminderCreate) -> Reminder:
        """Create exam/deadline reminder"""
        reminder_id = str(uuid.uuid4())
        reminder = Reminder(
            reminder_id=reminder_id,
            user_id=reminder_data.user_id,
            title=reminder_data.title,
            description=reminder_data.description,
            exam_date=reminder_data.exam_date,
            subject=reminder_data.subject,
            priority=reminder_data.priority,
            created_at=datetime.utcnow()
        )
        
        await self.db.collection('reminders').document(reminder_id).set(reminder.dict())
        return reminder

    async def get_upcoming_reminders(self, user_id: str) -> List[Reminder]:
        """Get upcoming reminders for user"""
        query = self.db.collection('reminders')\
            .where(filter=FieldFilter('user_id', '==', user_id))\
            .where(filter=FieldFilter('exam_date', '>=', datetime.utcnow()))\
            .where(filter=FieldFilter('status', '==', 'active'))\
            .order_by('exam_date')
        
        docs = await query.get()
        return [Reminder(**doc.to_dict()) for doc in docs]

# Global service instance
firestore_service = FirestoreService()
