# Data validation utilities
"""
Data validation utilities
Pydantic validators and custom validation functions
"""

import re
from datetime import datetime, timedelta
from typing import Any, List, Optional
from pydantic import validator, ValidationError

class UserValidators:
    """Validators for user-related data"""
    
    @staticmethod
    def validate_name(name: str) -> str:
        """Validate user name"""
        if not name or not isinstance(name, str):
            raise ValueError("Name is required")
        
        name = name.strip()
        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(name) > 100:
            raise ValueError("Name must be less than 100 characters")
        
        # Only allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s'-]+$", name):
            raise ValueError("Name can only contain letters, spaces, hyphens, and apostrophes")
        
        return name.title()  # Capitalize properly
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email address"""
        if not email or not isinstance(email, str):
            raise ValueError("Email is required")
        
        email = email.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        
        return email
    
    @staticmethod
    def validate_subjects(subjects: List[str]) -> List[str]:
        """Validate list of subjects"""
        if not isinstance(subjects, list):
            raise ValueError("Subjects must be a list")
        
        if len(subjects) > 20:
            raise ValueError("Maximum 20 subjects allowed")
        
        validated_subjects = []
        for subject in subjects:
            if not isinstance(subject, str):
                continue
            
            subject = subject.strip().title()
            if len(subject) < 2 or len(subject) > 50:
                continue
            
            if re.match(r'^[a-zA-Z0-9\s&.-]+$', subject):
                validated_subjects.append(subject)
        
        return list(set(validated_subjects))  # Remove duplicates

class AcademicValidators:
    """Validators for academic-related data"""
    
    @staticmethod
    def validate_understanding_level(level: Any) -> int:
        """Validate understanding level (1-10)"""
        try:
            level = int(level)
        except (ValueError, TypeError):
            raise ValueError("Understanding level must be a number")
        
        if not 1 <= level <= 10:
            raise ValueError("Understanding level must be between 1 and 10")
        
        return level
    
    @staticmethod
    def validate_study_time(minutes: Any) -> int:
        """Validate study time in minutes"""
        try:
            minutes = int(minutes)
        except (ValueError, TypeError):
            raise ValueError("Study time must be a number")
        
        if minutes < 1:
            raise ValueError("Study time must be at least 1 minute")
        if minutes > 600:  # 10 hours max
            raise ValueError("Study time cannot exceed 10 hours")
        
        return minutes
    
    @staticmethod
    def validate_subject_topic(subject: str, topic: str) -> tuple:
        """Validate subject and topic names"""
        # Validate subject
        if not subject or not isinstance(subject, str):
            raise ValueError("Subject is required")
        
        subject = subject.strip().title()
        if len(subject) < 2 or len(subject) > 100:
            raise ValueError("Subject must be between 2 and 100 characters")
        
        if not re.match(r'^[a-zA-Z0-9\s&.-]+$', subject):
            raise ValueError("Subject contains invalid characters")
        
        # Validate topic
        if not topic or not isinstance(topic, str):
            raise ValueError("Topic is required")
        
        topic = topic.strip()
        if len(topic) < 3 or len(topic) > 200:
            raise ValueError("Topic must be between 3 and 200 characters")
        
        return subject, topic

class ConversationValidators:
    """Validators for conversation-related data"""
    
    @staticmethod
    def validate_message_content(content: str) -> str:
        """Validate message content"""
        if not content or not isinstance(content, str):
            raise ValueError("Message content is required")
        
        content = content.strip()
        if len(content) < 1:
            raise ValueError("Message cannot be empty")
        if len(content) > 5000:
            raise ValueError("Message too long (max 5000 characters)")
        
        # Basic content filtering
        prohibited_patterns = [
            r'\b(?:spam|scam|phishing)\b',
            r'\b(?:hack|crack|exploit)\b',
        ]
        
        for pattern in prohibited_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                raise ValueError("Message contains prohibited content")
        
        return content
    
    @staticmethod
    def validate_session_type(session_type: str) -> str:
        """Validate conversation session type"""
        valid_types = ["general", "study_session", "check_in", "exam_prep", "help"]
        
        if not session_type or session_type not in valid_types:
            return "general"  # Default fallback
        
        return session_type

class ReminderValidators:
    """Validators for reminder-related data"""
    
    @staticmethod
    def validate_exam_date(exam_date: datetime) -> datetime:
        """Validate exam/deadline date"""
        if not isinstance(exam_date, datetime):
            raise ValueError("Invalid date format")
        
        now = datetime.utcnow()
        
        # Can't be in the past (with 1 hour tolerance)
        if exam_date < now - timedelta(hours=1):
            raise ValueError("Exam date cannot be in the past")
        
        # Can't be more than 2 years in the future
        if exam_date > now + timedelta(days=730):
            raise ValueError("Exam date cannot be more than 2 years in the future")
        
        return exam_date
    
    @staticmethod
    def validate_reminder_title(title: str) -> str:
        """Validate reminder title"""
        if not title or not isinstance(title, str):
            raise ValueError("Reminder title is required")
        
        title = title.strip()
        if len(title) < 3:
            raise ValueError("Title must be at least 3 characters long")
        if len(title) > 200:
            raise ValueError("Title must be less than 200 characters")
        
        return title
    
    @staticmethod
    def validate_priority(priority: str) -> str:
        """Validate reminder priority"""
        valid_priorities = ["low", "medium", "high"]
        priority = priority.lower() if priority else "medium"
        
        if priority not in valid_priorities:
            return "medium"  # Default fallback
        
        return priority

class GeneralValidators:
    """General purpose validators"""
    
    @staticmethod
    def validate_pagination(page: int, limit: int) -> tuple:
        """Validate pagination parameters"""
        try:
            page = max(1, int(page))
        except (ValueError, TypeError):
            page = 1
        
        try:
            limit = max(1, min(100, int(limit)))  # Max 100 items per page
        except (ValueError, TypeError):
            limit = 10
        
        return page, limit
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> tuple:
        """Validate date range strings"""
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            # Default to last 7 days
            end = datetime.utcnow()
            start = end - timedelta(days=7)
            return start, end
        
        # Ensure start is before end
        if start >= end:
            end = start + timedelta(days=1)
        
        # Limit to maximum 1 year range
        if (end - start).days > 365:
            start = end - timedelta(days=365)
        
        return start, end
    
    @staticmethod
    def sanitize_search_query(query: str) -> str:
        """Sanitize search query"""
        if not query or not isinstance(query, str):
            return ""
        
        # Remove special characters, keep alphanumeric and spaces
        query = re.sub(r'[^\w\s]', ' ', query)
        
        # Collapse multiple spaces
        query = re.sub(r'\s+', ' ', query.strip())
        
        # Limit length
        return query[:100]

def validate_api_input(data: dict, required_fields: List[str]) -> dict:
    """Validate API input data"""
    errors = []
    
    # Check required fields
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"Field '{field}' is required")
    
    if errors:
        raise ValidationError(errors)
    
    return data
