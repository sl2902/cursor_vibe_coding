#!/usr/bin/env python3
"""
Simple script to test Milvus connection
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from pymilvus import connections, utility
from app.config import settings

def test_milvus_connection():
    """Test connection to Milvus"""
    print("🔍 Testing Milvus connection...")
    print(f"Host: {settings.milvus_host}")
    print(f"Port: {settings.milvus_port}")
    print(f"Username: {settings.milvus_username}")
    
    try:
        # Test connection
        connections.connect(
            alias="test",
            host=settings.milvus_host,
            port=settings.milvus_port,
            user=settings.milvus_username,
            password=settings.milvus_password,
            secure=True
        )
        
        print("✅ Successfully connected to Milvus!")
        
        # Check if connection is still active
        if connections.has_connection("test"):
            print("✅ Connection is still active")
            
            # Test if we can list collections using the connection
            try:
                # Use the connection alias for utility operations
                collections = utility.list_collections(using="test")
                print(f"📚 Found {len(collections)} collections: {collections}")
            except Exception as e:
                print(f"⚠️  Could not list collections: {e}")
                print("   This might be normal if no collections exist yet")
        else:
            print("❌ Connection was lost after initial connect")
        
        # Disconnect
        try:
            connections.disconnect("test")
            print("🔌 Disconnected from Milvus")
        except Exception as e:
            print(f"⚠️  Error during disconnect: {e}")
        
    except Exception as e:
        print(f"❌ Failed to connect to Milvus: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_milvus_connection() 