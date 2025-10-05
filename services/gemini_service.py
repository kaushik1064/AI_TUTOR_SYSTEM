# Google Gemini Pro AI
"""
Google Gemini Pro integration service
Handles AI conversations, emotional analysis, and personalized responses
"""

import asyncio
import json
import logging
from typing import List, Optional, Tuple, Dict
from datetime import datetime

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from backend.config import settings, GEMINI_CONFIG, SYSTEM_PROMPTS
from backend.models import Message, EmotionState, MessageRole, User, AcademicProgress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    """Google Gemini Pro service for conversational AI"""
    
    def __init__(self):
        """Initialize Gemini Pro service"""
        try:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(
                model_name="gemini-2.5-pro",
                generation_config={
                    "temperature": GEMINI_CONFIG["temperature"],
                    "max_output_tokens": GEMINI_CONFIG.get("max_tokens", 1000),
                }
            )
            logger.info("✅ Gemini Pro service initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini Pro: {e}")
            raise

    async def generate_response(
        self,
        user_message: str,
        conversation_history: List[Message],
        user_profile: User,
        context_type: str = "default",
        academic_context: Optional[List[AcademicProgress]] = None
    ) -> Tuple[str, Optional[EmotionState], Optional[int]]:
        """
        Generate personalized AI response using Gemini Pro
        
        Args:
            user_message: Current user message
            conversation_history: Previous conversation messages
            user_profile: User profile information
            context_type: Type of conversation (default, study_session, check_in)
            academic_context: Recent academic progress for personalization
            
        Returns:
            Tuple of (response_text, detected_emotion, understanding_level)
        """
        try:
            # Build conversation context
            system_prompt = self._build_system_prompt(
                user_profile, context_type, academic_context
            )
            
            # Prepare conversation history
            conversation_context = self._format_conversation_history(
                conversation_history, user_message
            )
            
            # Create full prompt
            full_prompt = f"{system_prompt}\n\n{conversation_context}"
            
            # Generate response
            response = await self._call_gemini_async(full_prompt)
            
            # Analyze emotional state and understanding
            emotion = await self._detect_emotion(user_message, response)
            understanding_level = await self._extract_understanding_level(
                user_message, response
            )
            
            logger.info(f"✅ Generated response for user {user_profile.user_id}")
            return response, emotion, understanding_level
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return self._get_fallback_response(), None, None

    async def _call_gemini_async(self, prompt: str) -> str:
        """Make async call to Gemini Pro API"""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(
                    prompt,
                    safety_settings={
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    }
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"❌ Gemini API call failed: {e}")
            raise

    def _build_system_prompt(
        self,
        user_profile: User,
        context_type: str,
        academic_context: Optional[List[AcademicProgress]] = None
    ) -> str:
        """Build personalized system prompt"""
        
        base_prompt = SYSTEM_PROMPTS.get(context_type, SYSTEM_PROMPTS["default"])
        
        # Add user context
        user_context = f"""
STUDENT PROFILE:
- Name: {user_profile.name}
- Academic Level: {user_profile.academic_level.value.replace('_', ' ').title()}
- Subjects: {', '.join(user_profile.subjects)}
- Study Style: {user_profile.learning_preferences.study_style.value}
- Total Study Time: {user_profile.total_study_time} minutes
- Conversations: {user_profile.conversations_count}
"""
        
        # Add recent academic progress if available
        if academic_context:
            recent_progress = "\nRECENT ACADEMIC PROGRESS:\n"
            for progress in academic_context[-5:]:  # Last 5 entries
                recent_progress += f"- {progress.subject}: {progress.topic} (Understanding: {progress.understanding_level}/10)\n"
            user_context += recent_progress
        
        return f"{base_prompt}\n\n{user_context}"

    def _format_conversation_history(
        self, 
        history: List[Message], 
        current_message: str
    ) -> str:
        """Format conversation history for context"""
        
        formatted_history = "CONVERSATION HISTORY:\n"
        
        # Include last 10 messages for context (within token limit)
        recent_messages = history[-10:] if len(history) > 10 else history
        
        for msg in recent_messages:
            role = "Student" if msg.role == MessageRole.user else "AI Tutor"
            formatted_history += f"{role}: {msg.content}\n"
            
            # Add emotional context if available
            if msg.emotion_detected:
                formatted_history += f"[Emotion detected: {msg.emotion_detected.value}]\n"
        
        formatted_history += f"\nStudent: {current_message}\nAI Tutor:"
        
        return formatted_history

    async def _detect_emotion(
        self, 
        user_message: str, 
        ai_response: str
    ) -> Optional[EmotionState]:
        """Detect emotional state from user message"""
        
        emotion_prompt = f"""
Analyze the emotional state of this student message. Consider context clues like:
- Word choice and tone
- Mentions of stress, confusion, excitement, frustration
- Academic pressure indicators
- Confidence or uncertainty signals

Student message: "{user_message}"

Respond with ONLY one of these emotions: happy, excited, neutral, confused, stressed, sad, frustrated

Emotion:"""
        
        try:
            emotion_response = await self._call_gemini_async(emotion_prompt)
            emotion_text = emotion_response.strip().lower()
            
            # Map to EmotionState enum
            for emotion in EmotionState:
                if emotion.value in emotion_text:
                    return emotion
                    
            return EmotionState.neutral
            
        except Exception as e:
            logger.error(f"❌ Error detecting emotion: {e}")
            return None

    async def _extract_understanding_level(
        self, 
        user_message: str, 
        ai_response: str
    ) -> Optional[int]:
        """Extract understanding level from conversation"""
        
        understanding_prompt = f"""
Based on this conversation, estimate the student's understanding level of the topic being discussed.
Consider:
- Confidence in their responses
- Questions they ask
- Clarity of their explanations
- Mistakes or misconceptions

Student: "{user_message}"
AI Response: "{ai_response}"

If no academic topic is being discussed, respond with "N/A".
Otherwise, respond with a number from 1-10 where:
1-3: Struggling, needs basic help
4-6: Developing understanding
7-8: Good grasp, minor gaps
9-10: Strong understanding

Understanding level:"""
        
        try:
            level_response = await self._call_gemini_async(understanding_prompt)
            level_text = level_response.strip()
            
            if "N/A" in level_text or "n/a" in level_text:
                return None
                
            # Extract number
            import re
            numbers = re.findall(r'\d+', level_text)
            if numbers:
                level = int(numbers[0])
                return max(1, min(10, level))  # Clamp to 1-10 range
                
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting understanding level: {e}")
            return None

    async def generate_session_summary(
        self, 
        messages: List[Message], 
        user_profile: User
    ) -> str:
        """Generate summary of study session or conversation"""
        
        conversation_text = "\n".join([
            f"{msg.role.value}: {msg.content}" for msg in messages
        ])
        
        summary_prompt = f"""
Create a concise summary of this tutoring conversation for {user_profile.name}.
Focus on:
- Main topics discussed
- Student's emotional state and progress
- Key learning achievements
- Areas that need more attention
- Overall session outcome

Keep it encouraging and actionable.

Conversation:
{conversation_text}

Summary:"""
        
        try:
            summary = await self._call_gemini_async(summary_prompt)
            return summary.strip()
        except Exception as e:
            logger.error(f"❌ Error generating summary: {e}")
            return "Study session completed successfully."

    async def generate_study_suggestions(
        self, 
        user_profile: User, 
        academic_progress: List[AcademicProgress],
        upcoming_exams: List = None
    ) -> List[str]:
        """Generate personalized study suggestions"""
        
        # Analyze progress patterns
        progress_summary = "\n".join([
            f"- {p.subject}: {p.topic} (Level: {p.understanding_level}/10)"
            for p in academic_progress[-10:]  # Recent progress
        ])
        
        exam_context = ""
        if upcoming_exams:
            exam_context = "\nUpcoming exams: " + ", ".join([
                f"{exam.subject} on {exam.exam_date.strftime('%Y-%m-%d')}"
                for exam in upcoming_exams
            ])
        
        suggestions_prompt = f"""
Generate 3-5 personalized study suggestions for {user_profile.name}.
Consider their:
- Academic level: {user_profile.academic_level.value}
- Learning style: {user_profile.learning_preferences.study_style.value}
- Recent progress: {progress_summary}
{exam_context}

Provide specific, actionable suggestions that match their learning style and current needs.

Suggestions:"""
        
        try:
            suggestions_response = await self._call_gemini_async(suggestions_prompt)
            
            # Parse suggestions into list
            suggestions = []
            for line in suggestions_response.split("\n"):
                line = line.strip()
                if line and (line.startswith("-") or line.startswith("•") or line.startswith("1.")):
                    # Clean up formatting
                    suggestion = line.lstrip("-•1234567890. ").strip()
                    if suggestion:
                        suggestions.append(suggestion)
            
            return suggestions[:5]  # Limit to 5 suggestions
            
        except Exception as e:
            logger.error(f"❌ Error generating suggestions: {e}")
            return [
                "Review your recent notes and highlight key concepts",
                "Practice active recall by explaining topics out loud",
                "Take regular breaks during study sessions",
                "Create visual summaries or mind maps for complex topics"
            ]

    def _get_fallback_response(self) -> str:
        """Provide fallback response when AI service fails"""
        return """I'm having a bit of trouble connecting right now, but I'm still here for you! 😊 
        
Could you tell me what you'd like to work on today? Whether it's:
- Reviewing a specific subject
- Planning your study schedule  
- Just having a chat about how you're feeling

I'm here to help however I can!"""

# Global service instance
gemini_service = GeminiService()
