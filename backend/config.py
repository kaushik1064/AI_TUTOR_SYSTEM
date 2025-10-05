# Configuration management
"""
Configuration management for AI Tutor System
Handles environment variables and application settings
"""

import os
import json
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import validator

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Google Cloud Configuration
    google_cloud_project: str = "modular-aileron-426301-u7"
    google_application_credentials: Optional[str] = None  # Add this line
    gemini_api_key: str = "AIzaSyC6gio_uYbwPit9og_VcH9zVDH9eZpthHQ"
    firebase_config: str = '{"type": "service_account","project_id": "modular-aileron-426301-u7","private_key_id": "ee9fbf4f8a3ef9f989d6136a4f1188493a2070b1","private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCJuC0yhawg67fC\nPAYyfMhZ3VtPEQzH54UWT51aCp7ZKUSldpyCh80RweCvjsFK6q6BAdFwE8cL+1H2\nvlJ2s+aem6caMN1yebf6Z5tJf32iMEJT1lgfmH9y+apB8tSsP1lgSQd16/H/G/k1\nizfEw7qaUNCzsHEezyhu90VV8GfkwYo14KFsKi0N8/vhMF4Z5/hxnTBNHPGsAFdy\nSmY32OVUY9amePsLMD8QduG7IHijDyBE5+kQRm6XxvtedtxpyjYJZgpx1sQiX0VV\nUFVVBf2U+43VKT/0DN15bUTd6+CvRQh+1vfLoIY3you82GykODbPzwG7j9L9Y46I\nk5n6Ge/xAgMBAAECggEAQSOiDSF4tuGHOxHVBJBM22R9yboQx4TUSCdED9CyLZj9\nZR3jDUJaVqnTMnZdKqgx/cb0XwSbwykOLZz7uDWDQUXyFctDEuBLit7ybiMlM0+M\nL8dUSy2AKsu4IhVPTmFwTsB8DOSaw8VhbFf6+tBxNIhBDpzIBICLaWD/pJRfL61B\nqF18OS1uK6/yf1x8fLeMb8jy/yPzF2OMOiIFPIVJHAaZnCz7d14JI7nmoJV9J1GH\nyCtojFYZ1kWdGegzOe1vLodduz8VFGpkvS8j3Az/sVy8x2S16FlH4LLIv0i9fcTe\nBMJVMzHAq/9kFCpLzj1f1Fi0IRi1fDnEgqjo7FEw+QKBgQC74h7EtApKYoMjHyqr\nMARbODYCeLv0+eorxkx5918xOXbCnttKonOx5auxV+siU3QOQrT1ilRb3/cL9XOS\ngfPm8yFirSIZHXHRlZxEAl1i+dq4oOfUdGGdZ8z5hS54NWRLD6LVJ39szYkdZrhO\n+jecyCQCAfspcbMKd4Yf59poWwKBgQC7pjwVpgZKBmqifPSrwHJ6dga2T3lD9M+Q\nEOS00NCaglvx1S8gPoGUs3LJO9BaasVYZA23MCInOrLz4+xNzXhiDI0yW+4x2m7j\nSv5vnBZDggCGJtkJehfEMKgP3h7WLdil929ALYLuhZ/Ck+nGSJ+tnySLhzJDudhA\nC5cZ/0TaowKBgAsmKu8/Q9EQMXn3EoAgFFIZbtMMuRKbdfLtDIK8VDDGmS6JYLf4\nFed7mommjvR1gVCLUtOzRrhA/Rb/lMEf5wpQaS3C2mAlKCjouOIsRcBm1TzZh4hK\n87P0gexYo95MRMxTfDUr59rcA4P0IYHGRWCPW9umpHHcJmS7nQDtsD87AoGAOKwm\n/17KDXdMo1Bb0Ldpm6SjuFHeTPDV8yu29wkNx2xReoMpHXLjTda4dyAyd+xBN8XY\nApht6C0pONGAX6sLjYk+55OuJ65RySGwIGMisjbEE8AN0nfmT6FmUIyEAamNAert\n1ZMpNQJ0Up67fuAWIairr9wgCSZKsmUNuJNI50MCgYATS4LEVaLBRzJHG38zU7Ck\nsLfi01m6x+qs2XccoRAUr8Py/RpiDFAMekoX1DRCF9NB+dbOVd2mvINw5i6vvEUJ\n+hqii6aaEcRktP6CLDuPCM3te5qF01jxncZnh3fS3HtlQUBoAx2mpmsLe2+EopF5\n29KhPXd5paUlfAmzRnz1Pw==\n-----END PRIVATE KEY-----\n","client_email": "firebase-adminsdk-fbsvc@modular-aileron-426301-u7.iam.gserviceaccount.com","client_id": "112173959078648306775","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40modular-aileron-426301-u7.iam.gserviceaccount.com","universe_domain": "googleapis.com"}'
    
    # Security Settings
    secret_key: str = "86-OzCYBq5gCxTaqIxuAyv600maTPXefAedOQ24t6jQ"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application Settings
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # AI Configuration
    max_conversation_length: int = 50
    embedding_dimension: int = 768
    temperature: float = 0.7
    max_tokens: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"
    
    @validator('firebase_config')
    def validate_firebase_config(cls, v):
        """Validate Firebase configuration JSON"""
        try:
            json.loads(v)
            return v
        except json.JSONDecodeError:
            raise ValueError("Invalid Firebase configuration JSON")
    
    def get_firebase_config(self) -> dict:
        """Parse Firebase configuration from JSON string"""
        return json.loads(self.firebase_config)

# Global settings instance
settings = Settings()

# Gemini Pro Configuration

GEMINI_CONFIG = {
    "model": "gemini-2.5-flash",
    "temperature": settings.temperature,
    "max_tokens": settings.max_tokens,
    "safety_settings": [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH", 
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]
}


# System prompts for different conversation types
SYSTEM_PROMPTS = {
    "default": """You are an empathetic AI tutor and friend for students. Your personality:

🎯 CORE TRAITS:
- Warm, encouraging, and genuinely caring
- Use appropriate emojis to convey emotion
- Ask thoughtful follow-up questions
- Remember previous conversations and academic progress
- Detect emotional states (stress, confusion, excitement) and respond appropriately

📚 ACADEMIC SUPPORT:
- Help with study planning and organization
- Provide explanations in simple, relatable terms
- Encourage active learning through questions
- Track understanding levels (1-10 scale)
- Suggest personalized study techniques

💝 EMOTIONAL SUPPORT:
- Acknowledge feelings and validate experiences
- Offer encouragement during difficult times
- Celebrate achievements, both big and small
- Help manage academic stress and anxiety
- Be a positive, supportive presence

Remember: You're not just a tutor, you're a friend who happens to be really good at helping with academics!""",
    
    "study_session": """You are now in STUDY SESSION mode! 🎯

Your role:
- Keep the student focused and motivated
- Provide bite-sized explanations when asked
- Check understanding regularly
- Offer encouragement and praise effort
- Track study time and breaks
- Suggest when to take breaks (every 25-30 mins)

Stay energetic, supportive, and focused on learning goals!""",
    
    "check_in": """Time for a friendly check-in! 😊

Your focus:
- Ask about their day and how they're feeling
- Inquire about recent studies and understanding
- Check on upcoming exams or deadlines
- Offer emotional support if needed
- Help them plan their next study steps
- Be genuinely interested in their well-being

Keep it conversational and caring!"""
}
