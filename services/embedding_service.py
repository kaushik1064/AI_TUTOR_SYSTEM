# Text embeddings for search
"""
Embedding service for semantic search and personalization
Handles text embeddings for academic content and user preferences
"""

import logging
from typing import List, Optional, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from backend.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating and managing text embeddings"""
    
    def __init__(self):
        """Initialize embedding models"""
        try:
            # Use Google's embedding model or fallback to local model
            genai.configure(api_key=settings.gemini_api_key)
            self.use_google_embeddings = True
            logger.info("✅ Google embeddings initialized")
        except Exception as e:
            logger.warning(f"Google embeddings failed, using local model: {e}")
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.use_google_embeddings = False
                logger.info("✅ Local embedding model initialized")
            except Exception as e2:
                logger.error(f"❌ Failed to initialize any embedding model: {e2}")
                raise
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        try:
            if self.use_google_embeddings:
                return await self._generate_google_embedding(text)
            else:
                return self._generate_local_embedding(text)
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 768
    
    async def _generate_google_embedding(self, text: str) -> List[float]:
        """Generate embedding using Google's API"""
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Google embedding failed: {e}")
            raise
    
    def _generate_local_embedding(self, text: str) -> List[float]:
        """Generate embedding using local model"""
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Local embedding failed: {e}")
            raise
    
    async def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            return 0.0
    
    def find_most_similar(
        self, 
        query_embedding: List[float], 
        candidate_embeddings: List[List[float]], 
        top_k: int = 5
    ) -> List[int]:
        """Find most similar embeddings to query"""
        try:
            similarities = []
            for i, candidate in enumerate(candidate_embeddings):
                similarity = self.calculate_similarity(query_embedding, candidate)
                similarities.append((i, similarity))
            
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Return top-k indices
            return [idx for idx, _ in similarities[:top_k]]
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []

# Global embedding service instance
embedding_service = EmbeddingService()
