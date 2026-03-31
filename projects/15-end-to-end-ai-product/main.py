import hashlib
import os
import secrets
import sqlite3
from datetime import datetime

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"
USAGE_LIMIT_PER_DAY = 30
DB_PATH = "app.db"


class SignupRequest(BaseModel):
    email: str
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: str
    password: str


class AskRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            token TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            prompt_chars INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None
app = FastAPI(title="End-to-End AI Product", version="1.0.0")
init_db()


def get_current_user_id(authorization: str | None = Header(default=None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token.")

    token = authorization.replace("Bearer ", "", 1).strip()
    conn = get_db()
    row = conn.execute("SELECT id FROM users WHERE token = ?", (token,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return int(row["id"])


def enforce_daily_usage_limit(user_id: int) -> None:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    conn = get_db()
    row = conn.execute(
        "SELECT COUNT(*) AS cnt FROM usage_logs WHERE user_id = ? AND created_at LIKE ?",
        (user_id, f"{today}%"),
    ).fetchone()
    conn.close()
    if row and int(row["cnt"]) >= USAGE_LIMIT_PER_DAY:
        raise HTTPException(status_code=429, detail="Daily usage limit reached.")


@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "AI Product API is running",
        "routes": "/signup, /login, /ask",
    }


@app.post("/signup")
def signup(req: SignupRequest) -> dict[str, str]:
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users(email, password_hash) VALUES(?, ?)",
            (req.email.strip().lower(), hash_password(req.password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=409, detail="User already exists.")

    conn.close()
    return {"message": "Signup successful."}


@app.post("/login")
def login(req: LoginRequest) -> dict[str, str]:
    conn = get_db()
    row = conn.execute(
        "SELECT id, password_hash FROM users WHERE email = ?",
        (req.email.strip().lower(),),
    ).fetchone()
    if not row or row["password_hash"] != hash_password(req.password):
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    token = secrets.token_urlsafe(24)
    conn.execute("UPDATE users SET token = ? WHERE id = ?", (token, int(row["id"])))
    conn.commit()
    conn.close()
    return {"token": token}


@app.post("/ask")
def ask(req: AskRequest, user_id: int = Depends(get_current_user_id)) -> dict[str, str]:
    if not client:
        raise HTTPException(status_code=500, detail="Missing GEMINI_API_KEY in environment.")

    enforce_daily_usage_limit(user_id)

    prompt = (
        "You are an AI assistant in a production app. "
        "Give concise, reliable answers. If uncertain, say so.\n\n"
        f"User prompt: {req.prompt}"
    )

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        answer = (response.text or "No answer generated.").strip()
    except Exception:
        raise HTTPException(status_code=502, detail="AI service unavailable.")

    conn = get_db()
    conn.execute(
        "INSERT INTO usage_logs(user_id, created_at, prompt_chars) VALUES(?, ?, ?)",
        (user_id, datetime.utcnow().isoformat(), len(req.prompt)),
    )
    conn.commit()
    conn.close()

    return {"answer": answer}
