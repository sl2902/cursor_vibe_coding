from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import logging
from app.config import settings
from app.routers.chat import router as chat_router
from app.services.milvus_service import milvus_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    # Startup
    logger.info("Starting up FastAPI Chatbot application...")
    try:
        # Initialize Milvus collection if connected
        if milvus_service.is_connected():
            milvus_service.create_collection()
            logger.info("Milvus collection initialized successfully")
        else:
            logger.warning("Milvus not connected - collection initialization skipped")
    except Exception as e:
        logger.error(f"Failed to initialize Milvus: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI Chatbot application...")


# Create FastAPI app
app = FastAPI(
    title="FastAPI Chatbot",
    description="A chatbot using OpenAI models with Milvus vector database",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FastAPI Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    """Serve the chat interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Chatbot Demo</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }

            .chat-container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 600px;
                height: 80vh;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }

            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }

            .chat-header h1 {
                font-size: 1.5rem;
                margin-bottom: 5px;
            }

            .chat-header p {
                opacity: 0.9;
                font-size: 0.9rem;
            }

            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            .message {
                display: flex;
                align-items: flex-start;
                gap: 10px;
            }

            .message.user {
                flex-direction: row-reverse;
            }

            .message-avatar {
                width: 35px;
                height: 35px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: white;
            }

            .message.user .message-avatar {
                background: #667eea;
            }

            .message.bot .message-avatar {
                background: #764ba2;
            }

            .message-content {
                background: #f8f9fa;
                padding: 12px 16px;
                border-radius: 18px;
                max-width: 70%;
                word-wrap: break-word;
            }

            .message.user .message-content {
                background: #667eea;
                color: white;
            }

            .message.bot .message-content {
                background: #f1f3f4;
                color: #333;
            }

            .chat-input {
                padding: 20px;
                border-top: 1px solid #eee;
                display: flex;
                gap: 10px;
            }

            .chat-input input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e1e5e9;
                border-radius: 25px;
                font-size: 14px;
                outline: none;
                transition: border-color 0.3s;
            }

            .chat-input input:focus {
                border-color: #667eea;
            }

            .chat-input button {
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-weight: bold;
                transition: transform 0.2s;
            }

            .chat-input button:hover {
                transform: translateY(-2px);
            }

            .chat-input button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }

            .loading {
                display: flex;
                align-items: center;
                gap: 8px;
                color: #666;
                font-style: italic;
            }

            .loading-dots {
                display: flex;
                gap: 4px;
            }

            .loading-dots span {
                width: 6px;
                height: 6px;
                background: #667eea;
                border-radius: 50%;
                animation: bounce 1.4s infinite ease-in-out;
            }

            .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
            .loading-dots span:nth-child(2) { animation-delay: -0.16s; }

            @keyframes bounce {
                0%, 80%, 100% { transform: scale(0); }
                40% { transform: scale(1); }
            }

            .error {
                background: #fee;
                color: #c33;
                padding: 10px;
                border-radius: 8px;
                margin: 10px 0;
                font-size: 14px;
            }

            .sources {
                font-size: 12px;
                color: #666;
                margin-top: 8px;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h1>🤖 FastAPI Chatbot</h1>
                <p>Powered by OpenAI & Milvus</p>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message bot">
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        Hello! I'm your AI assistant. I can help you with questions about FastAPI, Milvus, OpenAI, and more. What would you like to know?
                    </div>
                </div>
            </div>
            
            <div class="chat-input">
                <input 
                    type="text" 
                    id="messageInput" 
                    placeholder="Type your message here..."
                    onkeypress="handleKeyPress(event)"
                >
                <button id="sendButton" onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            const API_BASE_URL = 'http://localhost:8000/api/v1';
            const chatMessages = document.getElementById('chatMessages');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            function addMessage(content, isUser = false, sources = null, searchMetadata = null) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
                
                const avatar = document.createElement('div');
                avatar.className = 'message-avatar';
                avatar.textContent = isUser ? '👤' : '🤖';
                
                const messageContent = document.createElement('div');
                messageContent.className = 'message-content';
                messageContent.textContent = content;
                
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(messageContent);
                
                // Add sources if available
                if (sources && sources.length > 0) {
                    const sourcesDiv = document.createElement('div');
                    sourcesDiv.className = 'sources';
                    sourcesDiv.textContent = `Sources: ${sources.join(', ')}`;
                    messageContent.appendChild(sourcesDiv);
                }
                
                // Add search metadata for debugging
                if (searchMetadata && !isUser) {
                    const metadataDiv = document.createElement('div');
                    metadataDiv.className = 'sources';
                    metadataDiv.style.fontSize = '10px';
                    metadataDiv.style.opacity = '0.7';
                    
                    let metadataText = `DB Search: ${searchMetadata.documents_found}/${searchMetadata.total_documents_searched} docs (threshold: ${searchMetadata.similarity_threshold})`;
                    if (searchMetadata.documents_found > 0) {
                        metadataText += ` (best score: ${searchMetadata.highest_score.toFixed(3)})`;
                    }
                    if (!searchMetadata.search_successful) {
                        metadataText += ` - ${searchMetadata.reason}`;
                    }
                    
                    metadataDiv.textContent = metadataText;
                    messageContent.appendChild(metadataDiv);
                }
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function addLoadingMessage() {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message bot';
                messageDiv.id = 'loadingMessage';
                
                const avatar = document.createElement('div');
                avatar.className = 'message-avatar';
                avatar.textContent = '🤖';
                
                const messageContent = document.createElement('div');
                messageContent.className = 'message-content';
                messageContent.innerHTML = `
                    <div class="loading">
                        Thinking
                        <div class="loading-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                `;
                
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(messageContent);
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function removeLoadingMessage() {
                const loadingMessage = document.getElementById('loadingMessage');
                if (loadingMessage) {
                    loadingMessage.remove();
                }
            }

            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;
                
                // Add user message
                addMessage(message, true);
                messageInput.value = '';
                
                // Disable input while processing
                messageInput.disabled = true;
                sendButton.disabled = true;
                
                // Add loading message
                addLoadingMessage();
                
                try {
                    const response = await fetch(`${API_BASE_URL}/chat`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    // Remove loading message
                    removeLoadingMessage();
                    
                    // Add bot response
                    addMessage(data.response, false, data.sources, data.search_metadata);
                    
                } catch (error) {
                    console.error('Error:', error);
                    removeLoadingMessage();
                    addMessage('Sorry, I encountered an error. Please try again.', false);
                } finally {
                    // Re-enable input
                    messageInput.disabled = false;
                    sendButton.disabled = false;
                    messageInput.focus();
                }
            }

            // Check API health on page load
            async function checkHealth() {
                try {
                    const response = await fetch(`${API_BASE_URL}/health`);
                    const data = await response.json();
                    
                    if (data.status !== 'healthy') {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'error';
                        errorDiv.textContent = `API Health Check Failed: ${data.status}. Please ensure the server is running.`;
                        chatMessages.appendChild(errorDiv);
                    }
                } catch (error) {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error';
                    errorDiv.textContent = 'Cannot connect to the API server. Please ensure the server is running on http://localhost:8000';
                    chatMessages.appendChild(errorDiv);
                }
            }

            // Check health when page loads
            checkHealth();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True
    ) 