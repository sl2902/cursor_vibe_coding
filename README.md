# FastAPI Chatbot with Milvus and OpenAI

A modern chatbot application built with FastAPI, using OpenAI models for natural language processing and Milvus cloud as a vector database for document retrieval.

## Features

- 🤖 **AI-Powered Chat**: Uses OpenAI's GPT models for intelligent responses
- 🔍 **Vector Search**: Milvus cloud vector database for semantic document retrieval
- 🚀 **FastAPI Backend**: High-performance async API with automatic documentation
- 📚 **Document Context**: Retrieves relevant documents to provide informed responses
- 🔧 **Easy Setup**: Simple configuration with environment variables
- 📊 **Health Monitoring**: Built-in health check endpoint
- ☁️ **Cloud Ready**: Pre-configured for Milvus cloud instance
- ⚙️ **Flexible Configuration**: Configurable embedding dimensions for different models

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Milvus Cloud  │
│   (Client)      │◄──►│   Backend       │◄──►│   Vector DB     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │   (Embeddings   │
                       │   & Chat)       │
                       └─────────────────┘
```

## Prerequisites

- Python 3.11+
- UV package manager
- Milvus cloud instance (already configured)
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-vibe-coding
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key
   # Milvus cloud credentials are pre-configured
   ```

## Configuration

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_EMBEDDING_DIMENSION=1536

# Milvus Configuration (Cloud)
MILVUS_HOST=your_host
MILVUS_PORT=443
MILVUS_USERNAME=your_username
MILVUS_PASSWORD=your_password
MILVUS_COLLECTION_NAME=chatbot_documents

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
```

### Embedding Model Dimensions

Different OpenAI embedding models have different dimensions:

- `text-embedding-3-small`: 1536 dimensions
- `text-embedding-3-large`: 3072 dimensions
- `text-embedding-ada-002`: 1536 dimensions

Make sure to set `OPENAI_EMBEDDING_DIMENSION` to match your chosen embedding model.

## Running the Application

1. **Start the FastAPI server**
   ```bash
   python run.py
   ```

2. **Ingest sample data** (optional)
   ```bash
   python scripts/ingest_sample_data.py
   ```

3. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/v1/health

## API Endpoints

### POST `/api/v1/chat`
Send a message to the chatbot.

**Request:**
```json
{
  "message": "What is FastAPI?",
  "conversation_id": "optional_conversation_id"
}
```

**Response:**
```json
{
  "response": "FastAPI is a modern, fast web framework...",
  "conversation_id": "optional_conversation_id",
  "sources": ["doc_001"]
}
```

### GET `/api/v1/health`
Check the health status of the application.

**Response:**
```json
{
  "status": "healthy",
  "milvus_connected": true,
  "openai_configured": true
}
```

## Project Structure

```
fastapi-vibe-coding/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── main.py           # FastAPI application
│   ├── models.py         # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── chat.py       # Chat endpoints
│   └── services/
│       ├── __init__.py
│       ├── chat_service.py    # Chat orchestration
│       ├── milvus_service.py  # Vector database operations
│       └── openai_service.py  # OpenAI API integration
├── scripts/
│   ├── __init__.py
│   └── ingest_sample_data.py  # Sample data ingestion
├── requirements.txt
├── env.example
└── README.md
```

## Usage Examples

### Using curl
```bash
# Send a chat message
curl -X POST "http://localhost:8000/api/v1/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is FastAPI?"}'

# Check health
curl "http://localhost:8000/api/v1/health"
```

### Using Python requests
```python
import requests

# Send a message
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"message": "What is FastAPI?"}
)
print(response.json())

# Check health
health = requests.get("http://localhost:8000/api/v1/health")
print(health.json())
```

## Development

### Adding New Documents
To add your own documents to the vector database:

1. Create a document ingestion script similar to `scripts/ingest_sample_data.py`
2. Format your documents with `id`, `content`, and optional `metadata`
3. Use the `chat_service.ingest_documents()` method

### Customizing the Chatbot
- Modify the system prompt in `openai_service.py`
- Adjust the number of similar documents retrieved in `chat_service.py`
- Change the embedding model and dimension in the configuration

### Switching Embedding Models
To use a different embedding model:

1. Update `OPENAI_EMBEDDING_MODEL` in your `.env` file
2. Update `OPENAI_EMBEDDING_DIMENSION` to match the new model
3. Recreate the Milvus collection (or create a new one with a different name)

## Error Handling

The application includes comprehensive error handling for:
- Milvus cloud connection failures
- OpenAI API errors
- Invalid requests
- Network timeouts

All errors are logged and appropriate HTTP status codes are returned.

## Performance Considerations

- Uses async/await for non-blocking I/O operations
- Implements connection pooling for Milvus cloud
- Caches OpenAI embeddings when possible
- Uses efficient vector search algorithms
- SSL-secured cloud connections

## Troubleshooting

### Common Issues

1. **Milvus Cloud Connection Error**
   - Ensure internet connectivity
   - Verify cloud instance is active
   - Check credentials in configuration

2. **OpenAI API Errors**
   - Verify your API key is valid
   - Check your OpenAI account has sufficient credits
   - Ensure the model name is correct

3. **Import Errors**
   - Make sure all dependencies are installed: `uv sync`
   - Verify you're using Python 3.11+

4. **Dimension Mismatch Errors**
   - Ensure `OPENAI_EMBEDDING_DIMENSION` matches your embedding model
   - Recreate the collection if switching models

### Debug Mode
Enable debug logging by modifying the logging level in `app/main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
