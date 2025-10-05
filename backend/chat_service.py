# Chat conversation handler
"""
Chat service for handling conversations
Manages conversation flow, context, and AI integration
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from backend.models import *
from services.gemini_service import gemini_service
from services.firestore_service import firestore_service

logger = logging.getLogger(__name__)

class ChatService:
    """Service for managing chat conversations"""
    
    def __init__(self):
        self.active_sessions = {}  # In-memory session cache
    
    async def start_conversation(
        self, 
        user_id: str, 
        session_type: str = "general"
    ) -> Conversation:
        """Start a new conversation session"""
        try:
            conversation_data = ConversationCreate(
                user_id=user_id,
                session_type=session_type
            )
            
            conversation = await firestore_service.create_conversation(conversation_data)
            
            # Cache active session
            self.active_sessions[conversation.conversation_id] = {
                "user_id": user_id,
                "session_type": session_type,
                "start_time": datetime.utcnow(),
                "message_count": 0
            }
            
            logger.info(f"Started conversation {conversation.conversation_id} for user {user_id}")
            return conversation
            
        except Exception as e:
            logger.error(f"Failed to start conversation: {e}")
            raise
    
    async def process_message(
        self,
        conversation_id: str,
        user_message: str,
        user_profile: User
    ) -> ChatResponse:
        """Process user message and generate AI response"""
        try:
            # Get conversation history
            conversations = await firestore_service.get_conversation_history(user_profile.user_id)
            current_conversation = next(
                (c for c in conversations if c.conversation_id == conversation_id), 
                None
            )
            
            if not current_conversation:
                raise ValueError("Conversation not found")
            
            # Get academic context for personalization
            academic_progress = await firestore_service.get_user_progress(user_profile.user_id)
            
            # Get session info
            session_info = self.active_sessions.get(conversation_id, {})
            session_type = session_info.get("session_type", "general")
            
            # Generate AI response using Gemini
            ai_response, emotion, understanding_level = await gemini_service.generate_response(
                user_message=user_message,
                conversation_history=current_conversation.messages,
                user_profile=user_profile,
                context_type=session_type,
                academic_context=academic_progress
            )
            
            # Save user message
            user_msg = Message(
                role=MessageRole.user,
                content=user_message,
                emotion_detected=emotion,
                understanding_level=understanding_level
            )
            await firestore_service.add_message(conversation_id, user_msg)
            
            # Save AI response
            ai_msg = Message(
                role=MessageRole.assistant,
                content=ai_response
            )
            await firestore_service.add_message(conversation_id, ai_msg)
            
            # Update session info
            if conversation_id in self.active_sessions:
                self.active_sessions[conversation_id]["message_count"] += 2
            
            # Generate suggestions periodically
            suggestions = []
            message_count = session_info.get("message_count", 0)
            if message_count > 0 and message_count % 6 == 0:  # Every 3 exchanges
                suggestions = await gemini_service.generate_study_suggestions(
                    user_profile, academic_progress[-5:] if academic_progress else []
                )
            
            # Update user activity
            await firestore_service.update_user_activity(user_profile.user_id)
            
            return ChatResponse(
                response=ai_response,
                emotion_detected=emotion,
                understanding_level=understanding_level,
                suggestions=suggestions,
                session_id=conversation_id
            )
            
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return ChatResponse(
                response="I'm having trouble right now, but I'm still here to help! Could you try asking that again?",
                session_id=conversation_id
            )
    
    async def end_session(self, conversation_id: str, user_profile: User) -> str:
        """End conversation session and generate summary"""
        try:
            # Get conversation
            conversations = await firestore_service.get_conversation_history(user_profile.user_id)
            conversation = next(
                (c for c in conversations if c.conversation_id == conversation_id), 
                None
            )
            
            if not conversation:
                return "Session ended."
            
            # Generate session summary
            summary = await gemini_service.generate_session_summary(
                conversation.messages, user_profile
            )
            
            # Update conversation with summary
            await firestore_service.db.collection('conversations').document(conversation_id).update({
                'session_summary': summary,
                'is_active': False,
                'updated_at': datetime.utcnow()
            })
            
            # Remove from active sessions
            if conversation_id in self.active_sessions:
                del self.active_sessions[conversation_id]
            
            logger.info(f"Ended session {conversation_id}")
            return summary
            
        except Exception as e:
            logger.error(f"Failed to end session: {e}")
            return "Session ended successfully."
    
    def get_active_sessions(self, user_id: str) -> List[str]:
        """Get active session IDs for user"""
        return [
            session_id for session_id, info in self.active_sessions.items()
            if info["user_id"] == user_id
        ]

# Global chat service instance
chat_service = ChatService()
