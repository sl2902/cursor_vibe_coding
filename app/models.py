from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None
    sources: Optional[List[str]] = None
    search_metadata: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    status: str
    milvus_connected: bool
    openai_configured: bool


class Document(BaseModel):
    id: str
    content: str
    metadata: Optional[dict] = None 