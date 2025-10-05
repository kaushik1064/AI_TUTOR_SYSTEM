# Progress analytics service
"""
Analytics service for generating student reports and insights
Processes academic data and generates meaningful statistics
"""

import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
import statistics

from backend.models import *
from services.firestore_service import firestore_service
from services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for generating analytics and reports"""
    
    async def generate_progress_report(
        self, 
        user_id: str, 
        days: int = 7
    ) -> Dict[str, Any]:
        """Generate comprehensive progress report"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Get user data
            user = await firestore_service.get_user(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Get academic progress
            progress_data = await firestore_service.get_user_progress(user_id, days)
            
            # Get conversations
            conversations = await firestore_service.get_conversation_history(user_id, 20)
            
            # Get reminders
            reminders = await firestore_service.get_upcoming_reminders(user_id)
            
            # Calculate study statistics
            study_stats = self._calculate_study_stats(progress_data)
            
            # Calculate emotional statistics
            emotional_stats = self._calculate_emotional_stats(conversations)
            
            # Generate AI insights and recommendations
            recommendations = await self._generate_recommendations(
                user, progress_data, conversations, reminders
            )
            
            # Compile report
            report = {
                "user_name": user.name,
                "report_period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                },
                "study_statistics": study_stats,
                "emotional_wellbeing": emotional_stats,
                "upcoming_events": [
                    {
                        "title": r.title,
                        "subject": r.subject,
                        "date": r.exam_date.isoformat(),
                        "days_until": (r.exam_date - datetime.utcnow()).days,
                        "priority": r.priority.value
                    }
                    for r in reminders[:5]
                ],
                "ai_recommendations": recommendations,
                "achievements": self._identify_achievements(progress_data, study_stats),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate progress report: {e}")
            raise
    
    def _calculate_study_stats(self, progress_data: List[AcademicProgress]) -> Dict[str, Any]:
        """Calculate study-related statistics"""
        if not progress_data:
            return {
                "total_study_time": 0,
                "session_count": 0,
                "average_session_duration": 0,
                "subjects_studied": [],
                "understanding_trend": {},
                "most_studied_subject": None,
                "average_understanding": 0
            }
        
        total_time = sum(p.time_spent for p in progress_data)
        session_count = len(progress_data)
        avg_duration = total_time / session_count if session_count > 0 else 0
        
        # Subject analysis
        subject_time = {}
        subject_understanding = {}
        
        for progress in progress_data:
            subject = progress.subject
            if subject not in subject_time:
                subject_time[subject] = 0
                subject_understanding[subject] = []
            
            subject_time[subject] += progress.time_spent
            subject_understanding[subject].append(progress.understanding_level)
        
        # Understanding trends
        understanding_trends = {}
        for subject, levels in subject_understanding.items():
            understanding_trends[subject] = {
                "average": statistics.mean(levels),
                "trend": levels,  # Raw data for trend analysis
                "latest": levels[-1] if levels else 0
            }
        
        most_studied = max(subject_time.items(), key=lambda x: x[1])[0] if subject_time else None
        
        overall_understanding = statistics.mean([
            p.understanding_level for p in progress_data
        ]) if progress_data else 0
        
        return {
            "total_study_time": total_time,
            "session_count": session_count,
            "average_session_duration": round(avg_duration, 1),
            "subjects_studied": list(subject_time.keys()),
            "understanding_trends": understanding_trends,
            "most_studied_subject": most_studied,
            "average_understanding": round(overall_understanding, 1),
            "subject_breakdown": [
                {
                    "subject": subject,
                    "time_spent": time,
                    "percentage": round((time / total_time) * 100, 1) if total_time > 0 else 0
                }
                for subject, time in subject_time.items()
            ]
        }
    
    def _calculate_emotional_stats(self, conversations: List[Conversation]) -> Dict[str, Any]:
        """Calculate emotional wellbeing statistics"""
        emotion_counts = {}
        total_messages = 0
        recent_emotions = []
        
        for conversation in conversations:
            for message in conversation.messages:
                if message.role == MessageRole.user and message.emotion_detected:
                    emotion = message.emotion_detected.value
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                    recent_emotions.append(emotion)
                    total_messages += 1
        
        # Calculate emotional distribution
        emotion_distribution = {}
        for emotion, count in emotion_counts.items():
            emotion_distribution[emotion] = {
                "count": count,
                "percentage": round((count / total_messages) * 100, 1) if total_messages > 0 else 0
            }
        
        # Determine dominant emotion
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "neutral"
        
        # Recent emotional trend (last 10 messages)
        recent_trend = recent_emotions[-10:] if len(recent_emotions) >= 10 else recent_emotions
        
        return {
            "emotion_distribution": emotion_distribution,
            "dominant_emotion": dominant_emotion,
            "recent_emotional_trend": recent_trend,
            "total_interactions": total_messages,
            "emotional_variety": len(emotion_counts),  # How many different emotions expressed
        }
    
    async def _generate_recommendations(
        self,
        user: User,
        progress_data: List[AcademicProgress],
        conversations: List[Conversation],
        reminders: List[Reminder]
    ) -> List[str]:
        """Generate AI-powered recommendations"""
        try:
            recommendations = await gemini_service.generate_study_suggestions(
                user, progress_data, reminders
            )
            return recommendations
        except Exception as e:
            logger.error(f"Failed to generate AI recommendations: {e}")
            return [
                "Continue your regular study routine",
                "Take breaks every 25-30 minutes during study sessions",
                "Review topics where understanding is below 7/10",
                "Prepare early for upcoming exams"
            ]
    
    def _identify_achievements(self, progress_data: List[AcademicProgress], study_stats: Dict) -> List[str]:
        """Identify student achievements"""
        achievements = []
        
        # Study time achievements
        total_time = study_stats.get("total_study_time", 0)
        if total_time >= 300:  # 5+ hours
            achievements.append("🎯 Dedicated Learner - Studied 5+ hours this week!")
        elif total_time >= 180:  # 3+ hours
            achievements.append("📚 Consistent Student - Great study habits!")
        
        # Understanding achievements
        avg_understanding = study_stats.get("average_understanding", 0)
        if avg_understanding >= 8.5:
            achievements.append("🌟 Excellence Achiever - Outstanding understanding levels!")
        elif avg_understanding >= 7.5:
            achievements.append("✨ Strong Performer - Great grasp of concepts!")
        
        # Subject variety
        subjects_count = len(study_stats.get("subjects_studied", []))
        if subjects_count >= 4:
            achievements.append("🎨 Multi-Subject Master - Excelling across multiple subjects!")
        elif subjects_count >= 2:
            achievements.append("📖 Well-Rounded Student - Balancing multiple subjects!")
        
        # Consistency achievements
        session_count = study_stats.get("session_count", 0)
        if session_count >= 10:
            achievements.append("🔥 Study Streak Champion - Consistent daily practice!")
        elif session_count >= 5:
            achievements.append("⭐ Regular Learner - Building great study habits!")
        
        # High understanding in specific topics
        high_understanding_topics = [
            p for p in progress_data if p.understanding_level >= 9
        ]
        if high_understanding_topics:
            subject = high_understanding_topics[0].subject
            achievements.append(f"🏆 {subject} Expert - Mastered challenging concepts!")
        
        return achievements if achievements else ["🌱 Learning Journey Started - Keep up the great work!"]

# Global analytics service instance
analytics_service = AnalyticsService()
