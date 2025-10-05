# Database connection manager
"""
Database connection and initialization
Handles Firestore setup and connection management
"""

import asyncio
import logging
from typing import Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore
from backend.config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database connection manager"""
    
    def __init__(self):
        self.db = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize database connection"""
        if self._initialized:
            return
            
        try:
            # Initialize Firebase Admin SDK
            if not firebase_admin._apps:
                firebase_config = settings.get_firebase_config()
                cred = credentials.Certificate(firebase_config)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.AsyncClient()
            self._initialized = True
            logger.info("✅ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check database connection health"""
        try:
            # Simple read operation to test connection
            await self.db.collection('health_check').limit(1).get()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def get_client(self):
        """Get database client"""
        if not self._initialized:
            raise Exception("Database not initialized")
        return self.db

# Global database manager
db_manager = DatabaseManager()
