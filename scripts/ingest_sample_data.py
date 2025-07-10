#!/usr/bin/env python3
"""
Sample data ingestion script for the FastAPI Chatbot.
This script demonstrates how to ingest documents into Milvus.
"""

import asyncio
import sys
import os
from typing import List, Dict, Any

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.chat_service import chat_service


async def ingest_sample_documents():
    """Ingest sample documents into Milvus"""
    sample_documents = [
        {
            "id": "doc_001",
            "content": "FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints. It was created by Sebastián Ramírez and is designed to be easy to use and highly performant. FastAPI supports async/await, automatic API documentation with Swagger UI, and data validation with Pydantic.",
            "metadata": {"source": "fastapi_docs", "category": "framework", "tags": ["python", "api", "web"]}
        },
        {
            "id": "doc_002", 
            "content": "Milvus is an open-source vector database designed for AI applications. It provides similarity search and analytics for unstructured data, making it ideal for machine learning applications. Milvus supports various distance metrics including cosine similarity, Euclidean distance, and inner product. It can handle billions of vectors and supports both CPU and GPU-based search.",
            "metadata": {"source": "milvus_docs", "category": "database", "tags": ["vector", "ai", "search"]}
        },
        {
            "id": "doc_003",
            "content": "OpenAI provides powerful language models like GPT-3.5 and GPT-4 that can understand and generate human-like text. These models are trained on vast amounts of data and can perform various natural language processing tasks including text generation, summarization, translation, and question answering. The models can be accessed via API with different pricing tiers.",
            "metadata": {"source": "openai_docs", "category": "ai", "tags": ["llm", "nlp", "api"]}
        },
        {
            "id": "doc_004",
            "content": "Vector databases store and retrieve high-dimensional vectors efficiently. They are essential for AI applications that need to find similar items, such as recommendation systems, image search, and semantic search. Popular vector databases include Pinecone, Weaviate, Qdrant, and Milvus. They support operations like similarity search, filtering, and real-time updates.",
            "metadata": {"source": "vector_db_docs", "category": "database", "tags": ["vector", "search", "ai"]}
        },
        {
            "id": "doc_005",
            "content": "Embeddings are numerical representations of text, images, or other data that capture semantic meaning. They allow computers to understand relationships between different pieces of information. OpenAI's text-embedding-3-small model creates 1536-dimensional embeddings that can be used for semantic search, clustering, and similarity matching. Embeddings are the foundation of modern AI applications.",
            "metadata": {"source": "ml_docs", "category": "machine_learning", "tags": ["embeddings", "ai", "semantic"]}
        },
        {
            "id": "doc_006",
            "content": "UV is a fast Python package installer and resolver written in Rust. It's designed to be a drop-in replacement for pip and can install packages up to 10-100x faster than pip. UV supports virtual environments, dependency resolution, and can generate lock files. It's particularly useful for Python projects that need fast dependency management and reproducible builds.",
            "metadata": {"source": "uv_docs", "category": "tools", "tags": ["python", "package_manager", "rust"]}
        },
        {
            "id": "doc_007",
            "content": "Retrieval-Augmented Generation (RAG) combines information retrieval with text generation. The system first searches a knowledge base for relevant documents, then uses that context to generate more accurate and informed responses. RAG systems typically use vector databases for semantic search and large language models for text generation. This approach improves answer quality and reduces hallucination.",
            "metadata": {"source": "rag_docs", "category": "ai", "tags": ["rag", "retrieval", "generation"]}
        },
        {
            "id": "doc_008",
            "content": "Similarity thresholds in vector search help filter out low-quality matches. When searching for relevant documents, a similarity score (like cosine similarity) indicates how well a document matches the query. Setting a threshold (e.g., 0.3) ensures only documents with sufficient relevance are used. This improves response quality and prevents irrelevant information from being included in AI responses.",
            "metadata": {"source": "search_docs", "category": "search", "tags": ["similarity", "threshold", "filtering"]}
        },
        {
            "id": "doc_009",
            "content": "FastAPI Chatbot is a RAG application that combines FastAPI, OpenAI models, and Milvus vector database. The system uses OpenAI embeddings for semantic search, stores documents in Milvus, and generates responses with ChatGPT. It includes features like similarity thresholds, search metadata logging, and a web interface. The project uses UV for dependency management and includes comprehensive error handling and monitoring.",
            "metadata": {"source": "project_docs", "category": "project", "tags": ["fastapi", "chatbot", "rag", "uv"]}
        },
        {
            "id": "doc_010",
            "content": "Pydantic is a data validation library for Python that uses type annotations. It's commonly used with FastAPI for request/response validation and serialization. Pydantic v2 introduced significant performance improvements and new features like computed fields, model serialization, and custom validators. It's essential for building robust APIs with automatic data validation and documentation.",
            "metadata": {"source": "pydantic_docs", "category": "library", "tags": ["validation", "serialization", "fastapi"]}
        }
    ]
    
    print("Ingesting sample documents into Milvus...")
    success = await chat_service.ingest_documents(sample_documents)
    
    if success:
        print("✅ Successfully ingested sample documents!")
        print(f"📄 Ingested {len(sample_documents)} documents")
        print("\nYou can now test the chatbot with questions like:")
        print("- 'What is FastAPI?'")
        print("- 'Tell me about Milvus'")
        print("- 'What are embeddings?'")
        print("- 'How does UV work?'")
        print("- 'What is RAG?'")
        print("- 'Explain similarity thresholds'")
        print("- 'Tell me about this project'")
        print("- 'What is Pydantic?'")
    else:
        print("❌ Failed to ingest documents. Please check your configuration.")


if __name__ == "__main__":
    asyncio.run(ingest_sample_documents()) 