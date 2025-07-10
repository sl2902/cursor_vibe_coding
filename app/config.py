from pydantic_settings import BaseSettings
from typing import Optional
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file explicitly with absolute path
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str  # Required - no default
    openai_model: str = "gpt-3.5-turbo"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_embedding_dimension: int = 1536
    
    # Milvus Configuration (Cloud)
    milvus_host: str
    milvus_port: int = 443
    milvus_username: str
    milvus_password: str
    milvus_collection_name: str = "chatbot_documents"
    
    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Settings() loads values from environment variables and .env file
settings = Settings()  # type: ignore

# Debug: Log the API key (masked for security)
masked_key = settings.openai_api_key[:10] + "..." + settings.openai_api_key[-4:] if len(settings.openai_api_key) > 14 else "***"
logger.info(f"Loaded OpenAI API key: {masked_key}")
logger.info(f"Loaded Milvus host: {settings.milvus_host}") 