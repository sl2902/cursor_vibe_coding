#!/usr/bin/env python3
"""
Test script to check .env file loading
"""

import os
from dotenv import load_dotenv

# Load .env file manually
load_dotenv()

print("🔍 Testing .env file loading...")
print(f"OPENAI_API_KEY from os.environ: {os.getenv('OPENAI_API_KEY', 'NOT_FOUND')[:20]}...")

# Test Pydantic Settings
from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    openai_api_key: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False

try:
    settings = TestSettings()
    masked_key = settings.openai_api_key[:10] + "..." + settings.openai_api_key[-4:] if len(settings.openai_api_key) > 14 else "***"
    print(f"OPENAI_API_KEY from Pydantic: {masked_key}")
except Exception as e:
    print(f"Error loading settings: {e}") 