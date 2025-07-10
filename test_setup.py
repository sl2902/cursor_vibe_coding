#!/usr/bin/env python3
"""
Test script to verify the FastAPI Chatbot setup.
Run this script to check if all dependencies and configurations are correct.
"""

import sys
import os
from typing import List

def test_imports() -> bool:
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    try:
        import pydantic_settings
        print("✅ Pydantic Settings imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic Settings import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import pymilvus
        print("✅ PyMilvus imported successfully")
    except ImportError as e:
        print(f"❌ PyMilvus import failed: {e}")
        return False
    
    try:
        import dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    return True


def test_configuration() -> bool:
    """Test if configuration can be loaded"""
    print("\n🔧 Testing configuration...")
    
    try:
        # Add the current directory to Python path
        sys.path.insert(0, os.path.dirname(__file__))
        
        from app.config import settings
        print("✅ Configuration loaded successfully")
        
        # Check if required settings are available
        if not hasattr(settings, 'openai_api_key'):
            print("⚠️  OPENAI_API_KEY not found in environment")
            print("   Please set OPENAI_API_KEY in your .env file")
            return False
        
        print(f"✅ Milvus host: {settings.milvus_host}:{settings.milvus_port}")
        print(f"✅ Collection name: {settings.milvus_collection_name}")
        print(f"✅ OpenAI model: {settings.openai_model}")
        print(f"✅ Embedding model: {settings.openai_embedding_model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_app_imports() -> bool:
    """Test if app modules can be imported"""
    print("\n📦 Testing app imports...")
    
    try:
        from app.models import ChatRequest, ChatResponse, HealthResponse
        print("✅ Models imported successfully")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from app.services.openai_service import openai_service
        print("✅ OpenAI service imported successfully")
    except Exception as e:
        print(f"❌ OpenAI service import failed: {e}")
        return False
    
    try:
        from app.services.milvus_service import milvus_service
        print("✅ Milvus service imported successfully")
    except Exception as e:
        print(f"❌ Milvus service import failed: {e}")
        return False
    
    try:
        from app.services.chat_service import chat_service
        print("✅ Chat service imported successfully")
    except Exception as e:
        print(f"❌ Chat service import failed: {e}")
        return False
    
    return True


def main():
    """Run all tests"""
    print("🚀 FastAPI Chatbot Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_configuration,
        test_app_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Start Milvus (if not already running)")
        print("2. Run: python -m app.main")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Create .env file: cp env.example .env")
        print("3. Set your OpenAI API key in .env file")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 