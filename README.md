# EduGenie

A lightweight AI-powered educational assistant built with FastAPI and a responsive HTML/CSS/JavaScript frontend.

## Features

- AI question answering
- Simplified concept explanations
- Quiz generation and scoring
- Educational text summarization
- Personalized learning roadmaps
- Responsive UI
- Optional cloud AI integration
- Offline/local demo mode without an API key
- FastAPI Swagger documentation

## Run

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

Swagger: http://127.0.0.1:8000/docs

## Optional cloud AI

Copy `.env.example` to `.env`, then add your API key:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

Restart the server.

## API endpoints

GET `/api/health`

POST `/api/chat`

POST `/api/quiz`

POST `/api/summarize`

POST `/api/roadmap`
