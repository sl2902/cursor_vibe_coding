from typing import List, Dict, Any, Optional
import logging
import json
from app.services.milvus_service import milvus_service
from app.services.openai_service import openai_service

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.milvus_service = milvus_service
        self.openai_service = openai_service
    
    async def process_message(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a user message and return a response"""
        try:
            # Get embedding for the user message
            query_embedding = self.openai_service.get_embedding(message)
            
            # Search for relevant documents in Milvus
            similar_docs = self.milvus_service.search_similar(query_embedding, limit=3)
            
            # Filter out low-quality matches (similarity threshold)
            SIMILARITY_THRESHOLD = 0.3  # Adjust this value as needed
            filtered_docs = []
            for doc in similar_docs:
                score = doc.get("score", 0)
                if score >= SIMILARITY_THRESHOLD:
                    filtered_docs.append(doc)
                else:
                    logger.info(f"Filtering out document {doc.get('id', 'unknown')} with low score: {score:.3f}")
            
            # Log search results for debugging
            logger.info(f"Found {len(similar_docs)} documents, filtered to {len(filtered_docs)} with score >= {SIMILARITY_THRESHOLD}")
            if filtered_docs:
                scores = [doc.get("score", 0) for doc in filtered_docs]
                logger.info(f"Filtered search scores: {scores}")
            
            # Build context from filtered documents
            context = self._build_context(filtered_docs)
            
            # Create messages for OpenAI
            messages = [
                {
                    "role": "user",
                    "content": message
                }
            ]
            
            # Get response from OpenAI
            response = self.openai_service.get_chat_completion(messages, context)
            
            # Extract sources and metadata from filtered documents
            sources = []
            search_metadata = {
                "documents_found": len(filtered_docs),
                "total_documents_searched": len(similar_docs),
                "highest_score": max([doc.get("score", 0) for doc in filtered_docs]) if filtered_docs else 0,
                "avg_score": sum([doc.get("score", 0) for doc in filtered_docs]) / len(filtered_docs) if filtered_docs else 0,
                "search_successful": True,
                "similarity_threshold": SIMILARITY_THRESHOLD
            }
            
            for doc in filtered_docs:
                doc_id = doc.get("id", "")
                if doc_id:
                    sources.append(doc_id)
            
            # If no documents found after filtering, add indicator
            if not filtered_docs:
                search_metadata["search_successful"] = False
                search_metadata["reason"] = f"No documents met similarity threshold ({SIMILARITY_THRESHOLD})"
                logger.warning(f"No relevant documents found for query: '{message[:50]}...' (threshold: {SIMILARITY_THRESHOLD})")
            
            return {
                "response": response,
                "conversation_id": conversation_id,
                "sources": sources,
                "search_metadata": search_metadata
            }
            
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try again.",
                "conversation_id": conversation_id,
                "sources": [],
                "search_metadata": {
                    "search_successful": False,
                    "reason": f"Error: {str(e)}",
                    "documents_found": 0,
                    "total_documents_searched": 0,
                    "highest_score": 0,
                    "avg_score": 0,
                    "similarity_threshold": 0.3
                }
            }
    
    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """Build context string from similar documents"""
        if not documents:
            return ""
        
        context_parts = []
        for doc in documents:
            content = doc.get("content", "")
            if content:
                context_parts.append(content)
        
        return "\n\n".join(context_parts)
    
    async def ingest_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Ingest documents into Milvus with embeddings"""
        try:
            # Get embeddings for all documents
            for doc in documents:
                content = doc.get("content", "")
                if content:
                    embedding = self.openai_service.get_embedding(content)
                    doc["embedding"] = embedding
                    # Convert metadata to JSON string for Milvus
                    if "metadata" in doc and doc["metadata"]:
                        doc["metadata"] = json.dumps(doc["metadata"])
            
            # Insert documents into Milvus
            self.milvus_service.insert_documents(documents)
            return True
            
        except Exception as e:
            logger.error(f"Failed to ingest documents: {e}")
            return False


chat_service = ChatService() 