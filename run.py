#!/usr/bin/env python3
"""
Startup script for the FastAPI Chatbot application.
This script provides an easy way to start the server with proper configuration.
"""

import os
import sys
import warnings
from pathlib import Path

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Start the FastAPI application"""
    print("🚀 Starting FastAPI Chatbot...")
    
    # Check if .env file exists
    env_file = current_dir / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("   Please create a .env file with your configuration:")
        print("   cp env.example .env")
        print("   Then edit .env with your OpenAI API key and other settings.")
        print()
    
    # Start the server
    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check your .env configuration")
        print("3. Ensure Milvus is running (if using local instance)")
        sys.exit(1)


if __name__ == "__main__":
    main() 