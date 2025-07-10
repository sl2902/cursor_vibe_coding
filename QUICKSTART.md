# Quick Start Guide

Get your FastAPI Chatbot running in 5 minutes!

## Prerequisites

- Python 3.11+
- OpenAI API key
- Cloud Milvus instance (already configured)

## Step 1: Setup Environment

```bash
# Clone and navigate to the project
cd fastapi-vibe-coding

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env with your OpenAI API key
# The Milvus cloud credentials are already configured
```

## Step 3: Start the Application

```bash
# Start the FastAPI server
python run.py
```

## Step 4: Ingest Sample Data

In a new terminal:

```bash
# Activate virtual environment
source .venv/bin/activate

# Ingest sample documents
python scripts/ingest_sample_data.py
```

## Step 5: Test the Chatbot

### Option A: Use the Web Interface
1. Open `frontend_example.html` in your browser
2. Start chatting!

### Option B: Use the API Directly

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Send a message
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is FastAPI?"}'
```

### Option C: Use Python

```python
import requests

# Send a message
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"message": "What is FastAPI?"}
)
print(response.json())
```

## Step 6: Explore the API

Visit http://localhost:8000/docs to see the interactive API documentation.

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Milvus Connection Error**
   - The cloud Milvus credentials are pre-configured
   - Check your internet connection
   - Verify the cloud instance is active

3. **OpenAI API Error**
   - Check your API key in `.env`
   - Ensure you have credits in your OpenAI account

4. **Port Already in Use**
   ```bash
   # Change port in .env or kill existing process
   lsof -ti:8000 | xargs kill -9
   ```

### Test Your Setup

Run the test script to verify everything is working:

```bash
python test_setup.py
```

## Next Steps

- Add your own documents to the vector database
- Customize the chatbot's responses
- Deploy to production
- Add authentication and rate limiting

## API Endpoints

- `POST /api/v1/chat` - Send a message
- `GET /api/v1/health` - Health check
- `GET /` - API info
- `GET /docs` - Interactive documentation

Happy coding! 🚀 