# Code Reviewer API

## Overview

**Code Reviewer** is an intelligent backend service built using FastAPI that performs automated AI-based code reviews. The service accepts source code files via REST API, analyzes them using Google Gemini, and stores the review results in a Supabase PostgreSQL database.

It is containerized with Docker and deployed serverlessly using Google Cloud Run, integrated with Cloud Build for continuous deployment. The system is designed to be lightweight, scalable, and developer-friendly.

---

## Live API

**Base URL:**  
`https://code-reviewer-628186848429.us-central1.run.app/`

Available monitoring endpoints:  
- Health: `GET /health`  
- Prometheus metrics: `GET /metrics`  

API documentation (Swagger UI):  
`GET /docs` → `https://code-reviewer-628186848429.us-central1.run.app/docs`

---

## Key Features

- Upload code files for AI-based review and feedback.  
- Uses Google Gemini (via the google-generativeai client) for intelligent code analysis.  
- Persists data (source code, metadata, AI responses) in Supabase (Postgres).  
- Built with FastAPI and Pydantic v2 for performance and type safety.  
- Includes `/health` endpoint for service monitoring.  
- Includes `/metrics` endpoint compatible with Prometheus for observability.  
- Automated build and deployment through Google Cloud Build and Cloud Run.  
- Secrets managed securely with Google Secret Manager.

---

## Architecture

| Component           | Technology / Service              |
|---------------------|-----------------------------------|
| Backend framework   | FastAPI                           |
| Database            | Supabase (PostgreSQL)             |
| ORM                 | SQLAlchemy                        |
| AI model            | Google Gemini                     |
| Containerization    | Docker                            |
| CI / CD             | Google Cloud Build                |
| Deployment          | Google Cloud Run                  |
| Secrets             | Google Secret Manager             |
| Monitoring          | Prometheus-compatible `/metrics`  |

---

## Endpoints

### POST /review
Accepts a source code file and optional language parameter. The service analyzes the code using Gemini and stores results in the database.

**Request (example using curl):**
```bash
curl -X POST \
  "https://code-reviewer-628186848429.us-central1.run.app/review?language=python" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@script.py;type=text/x-python"
```

**Successful response (example):**
```bash
{
  "id": 1,
  "filename": "script.py",
  "language": "python",
  "code_excerpt": "def add(a, b): return a + b",
  "parsed_report": {
    "summary": "Code is correct but lacks docstrings and type hints."
  },
  "raw_response": "...",
  "created_at": "2025-10-15T00:00:00"
}
```

**GET /health** - Returns a simple health check useful for uptime monitoring.
```bash
{
  "status": "healthy",
  "timestamp": "2025-10-15T12:34:56Z"
}
```

**GET /metrics** - Exposes Prometheus-compatible metrics (request counters, latencies, error counts, etc.). Use this URL as a Prometheus scrape target: <br>
`
https://code-reviewer-628186848429.us-central1.run.app/metrics
`

**GET /docs** - Interactive API documentation (Swagger UI): <br>
`https://code-reviewer-628186848429.us-central1.run.app/docs`

## Local Development

### Prerequisites
- Python 3.12+

- A virtual environment (venv)

- Docker (for container testing)

- Supabase account and credentials

- Google API key for Gemini (stored in Secret Manager for deployment or in .env for local dev)

### Setup

1. Clone the repo
```
git clone https://github.com/your-username/code-reviewer.git
cd code-reviewer
```

2. Create and activate a virtual environment:
```
python -m venv .venv
# for macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.text
```

4. Create a `.env` file in the project root for local development (do not commit `.env`):
```
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+psycopg2://username:password@host:port/database
```

5. Create tables:
```
from database import Base, engine
Base.metadata.create_all(bind=engine)
```

6. Run the server
```
uvicorn main:app --reload
```

7. Open API docs:
```
http://127.0.0.1:8000/docs
```

<hr>

```
Made by Sunny Gogoi
```