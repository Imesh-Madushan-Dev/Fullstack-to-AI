import os
import time
from collections import defaultdict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"
RATE_LIMIT_PER_MINUTE = 20


class TaskRequest(BaseModel):
    tasks: list[str] = Field(min_length=1, max_length=50)


class TaskPriority(BaseModel):
    task: str
    priority: str
    reason: str


class TaskResponse(BaseModel):
    items: list[TaskPriority]


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None
app = FastAPI(title="AI-Powered SaaS Feature", version="1.0.0")

# Simple in-memory IP rate limiter.
request_log: dict[str, list[float]] = defaultdict(list)


def enforce_rate_limit(ip: str) -> None:
    now = time.time()
    window_start = now - 60
    entries = [t for t in request_log[ip] if t >= window_start]
    if len(entries) >= RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    entries.append(now)
    request_log[ip] = entries


@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "AI task prioritizer is running.",
        "endpoint": "POST /api/prioritize",
    }


@app.post("/api/prioritize", response_model=TaskResponse)
def prioritize(req: TaskRequest, request: Request) -> TaskResponse:
    if not client:
        raise HTTPException(status_code=500, detail="Missing GEMINI_API_KEY in environment.")

    ip = request.client.host if request.client else "unknown"
    enforce_rate_limit(ip)

    prompt = f"""
You are a product assistant that prioritizes tasks.

For each task, assign priority as one of: High, Medium, Low.
Return strict JSON with this shape:
{{
  "items": [
    {{"task": "...", "priority": "High|Medium|Low", "reason": "short reason"}}
  ]
}}

Tasks:
{req.tasks}
""".strip()

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        text = (response.text or "").strip()
    except Exception:
        raise HTTPException(status_code=502, detail="AI service failed. Please retry.")

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise HTTPException(status_code=500, detail="Invalid AI response format.")

    import json

    try:
        parsed = json.loads(text[start : end + 1])
        return TaskResponse.model_validate(parsed)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not parse AI response.")
