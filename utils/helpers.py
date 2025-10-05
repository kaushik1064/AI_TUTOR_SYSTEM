# Common helper functions
"""
Utility helper functions
Common utilities used across the application
"""

import re
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import hashlib
import secrets

logger = logging.getLogger(__name__)

class DateHelper:
    """Date and time utility functions"""
    
    @staticmethod
    def get_days_until(target_date: datetime) -> int:
        """Get number of days until target date"""
        delta = target_date - datetime.utcnow()
        return delta.days
    
    @staticmethod
    def format_time_ago(timestamp: datetime) -> str:
        """Format timestamp as 'time ago' string"""
        now = datetime.utcnow()
        delta = now - timestamp
        
        if delta.days > 0:
            return f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
    
    @staticmethod
    def get_week_range(date: datetime = None) -> tuple:
        """Get start and end of week for given date"""
        if date is None:
            date = datetime.utcnow()
        
        # Get Monday of current week
        days_since_monday = date.weekday()
        monday = date - timedelta(days=days_since_monday)
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Get Sunday of current week
        sunday = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        return monday, sunday

class TextHelper:
    """Text processing utility functions"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        return text
    
    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from text (simple implementation)"""
        if not text:
            return []
        
        # Simple keyword extraction - remove stop words and get unique words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Return unique keywords
        unique_keywords = list(dict.fromkeys(keywords))
        return unique_keywords[:max_keywords]
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to maximum length"""
        if not text or len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def extract_numbers(text: str) -> List[float]:
        """Extract all numbers from text"""
        numbers = re.findall(r'-?\d+(?:\.\d+)?', text)
        return [float(num) for num in numbers]

class SecurityHelper:
    """Security utility functions"""
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate secure session ID"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_string(text: str) -> str:
        """Hash string using SHA-256"""
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove or replace unsafe characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip('. ')
        return filename[:255]  # Limit length

class ValidationHelper:
    """Data validation utility functions"""
    
    @staticmethod
    def validate_understanding_level(level: Any) -> bool:
        """Validate understanding level (1-10)"""
        try:
            level = int(level)
            return 1 <= level <= 10
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_study_time(minutes: Any) -> bool:
        """Validate study time in minutes"""
        try:
            minutes = int(minutes)
            return 1 <= minutes <= 600  # Max 10 hours
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_subject_name(subject: str) -> bool:
        """Validate subject name"""
        if not subject or not isinstance(subject, str):
            return False
        
        subject = subject.strip()
        if len(subject) < 2 or len(subject) > 100:
            return False
        
        # Only allow letters, numbers, spaces, and basic punctuation
        return re.match(r'^[a-zA-Z0-9\s.,&-]+$', subject) is not None

class StatisticsHelper:
    """Statistical calculation utilities"""
    
    @staticmethod
    def calculate_trend(values: List[float]) -> str:
        """Calculate trend direction from list of values"""
        if len(values) < 2:
            return "stable"
        
        # Simple linear trend calculation
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        if avg_second > avg_first * 1.1:
            return "improving"
        elif avg_second < avg_first * 0.9:
            return "declining"
        else:
            return "stable"
    
    @staticmethod
    def calculate_percentile(value: float, values: List[float]) -> float:
        """Calculate percentile of value in list"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        count_below = sum(1 for v in sorted_values if v < value)
        
        percentile = (count_below / len(values)) * 100
        return round(percentile, 1)
    
    @staticmethod
    def get_study_insights(progress_data: List[Dict]) -> Dict[str, Any]:
        """Generate study insights from progress data"""
        if not progress_data:
            return {}
        
        total_time = sum(p.get('time_spent', 0) for p in progress_data)
        avg_understanding = sum(p.get('understanding_level', 0) for p in progress_data) / len(progress_data)
        
        subjects = list(set(p.get('subject', '') for p in progress_data))
        
        return {
            'total_sessions': len(progress_data),
            'total_time_minutes': total_time,
            'average_understanding': round(avg_understanding, 1),
            'subjects_count': len(subjects),
            'avg_session_duration': round(total_time / len(progress_data), 1) if progress_data else 0
        }
