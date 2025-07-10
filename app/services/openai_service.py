from openai import OpenAI
from typing import List, Dict, Any
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self):
        # Debug: Log the API key being used
        masked_key = settings.openai_api_key[:10] + "..." + settings.openai_api_key[-4:] if len(settings.openai_api_key) > 14 else "***"
        logger.info(f"Initializing OpenAI service with API key: {masked_key}")
        
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.embedding_model = settings.openai_embedding_model
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text using OpenAI's embedding model"""
        try:
            logger.info(f"Getting embedding for text: {text[:50]}...")
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            logger.info("Embedding generated successfully")
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to get embedding: {e}")
            raise
    
    def get_chat_completion(self, messages: List[Dict[str, str]], context: str = "") -> str:
        """Get chat completion from OpenAI"""
        try:
            logger.info(f"Getting chat completion with {len(messages)} messages")
            # Add context to the system message if provided
            if context:
                system_message = {
                    "role": "system",
                    "content": f"You are a helpful assistant. Use the following context to answer the user's question: {context}"
                }
                messages = [system_message] + messages
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                max_tokens=1000,
                temperature=0.7
            )
            
            logger.info("Chat completion generated successfully")
            content = response.choices[0].message.content
            return content if content else "No response generated"
        except Exception as e:
            logger.error(f"Failed to get chat completion: {e}")
            raise
    
    def is_configured(self) -> bool:
        """Check if OpenAI is properly configured"""
        try:
            api_key = settings.openai_api_key
            masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
            logger.info(f"Checking OpenAI configuration. API key: {masked_key}")
            return bool(api_key) and api_key != "your_openai_api_key_here"
        except Exception as e:
            logger.error(f"Error checking OpenAI configuration: {e}")
            return False


openai_service = OpenAIService() 