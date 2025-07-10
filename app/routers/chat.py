from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse, HealthResponse
from app.services.chat_service import chat_service
from app.services.milvus_service import milvus_service
from app.services.openai_service import openai_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message and return a response"""
    try:
        result = await chat_service.process_message(
            message=request.message,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            sources=result["sources"],
            search_metadata=result.get("search_metadata")
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    try:
        # Test Milvus connection properly
        milvus_connected = False
        try:
            # Try to list collections to verify connection works
            from pymilvus import utility
            collections = utility.list_collections(using="default")
            milvus_connected = True
        except Exception as e:
            logger.warning(f"Milvus connection test failed: {e}")
            milvus_connected = False
        
        openai_configured = openai_service.is_configured()
        
        status = "healthy" if milvus_connected and openai_configured else "unhealthy"
        
        return HealthResponse(
            status=status,
            milvus_connected=milvus_connected,
            openai_configured=openai_configured
        )
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return HealthResponse(
            status="unhealthy",
            milvus_connected=False,
            openai_configured=False
        ) 