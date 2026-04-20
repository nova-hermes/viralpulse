"""ViralPulse Web Dashboard — FastAPI SaaS layer."""

import os
import json
import time
import sqlite3
import hashlib
import secrets
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Request, Depends, HTTPException, Form, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ─── Config ───────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "viralpulse.db"
DRAFTS_DIR = BASE_DIR / "data" / "drafts"
MEDIA_DIR = BASE_DIR / "data" / "media"

# Ensure dirs exist
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# ─── Database ─────────────────────────────────────────────────────────

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT DEFAULT '',
            plan TEXT DEFAULT 'free',
            videos_generated INTEGER DEFAULT 0,
            videos_limit INTEGER DEFAULT 5,
            is_owner INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            niche TEXT DEFAULT 'general',
            status TEXT DEFAULT 'pending',
            script TEXT,
            video_path TEXT,
            thumbnail_path TEXT,
            youtube_url TEXT,
            cost REAL DEFAULT 0.0,
            created_at TEXT DEFAULT (datetime('now')),
            completed_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()

# ─── Auth helpers ─────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_session(user_id: int) -> str:
    token = secrets.token_hex(32)
    expires = (datetime.utcnow() + timedelta(days=30)).isoformat()
    conn = get_db()
    conn.execute("INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
                 (token, user_id, expires))
    conn.commit()
    conn.close()
    return token

def get_current_user(session_token: Optional[str] = Cookie(None)) -> Optional[dict]:
    if not session_token:
        return None
    conn = get_db()
    row = conn.execute("""
        SELECT u.* FROM users u
        JOIN sessions s ON s.user_id = u.id
        WHERE s.token = ? AND s.expires_at > datetime('now')
    """, (session_token,)).fetchone()
    conn.close()
    return dict(row) if row else None

def require_user(session_token: Optional[str] = Cookie(None)) -> dict:
    user = get_current_user(session_token)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# ─── Plan definitions ─────────────────────────────────────────────────

PLANS = {
    "free": {"name": "Free", "price": 0, "limit": 5, "features": ["5 videos/month", "Watermarked", "720p"]},
    "starter": {"name": "Starter", "price": 29, "limit": 30, "features": ["30 videos/month", "No watermark", "1080p", "Priority queue"]},
    "pro": {"name": "Pro", "price": 79, "limit": 100, "features": ["100 videos/month", "No watermark", "1080p", "Priority queue", "Custom niches"]},
    "agency": {"name": "Agency", "price": 199, "limit": 999999, "features": ["Unlimited videos", "No watermark", "1080p", "Priority queue", "Custom niches", "API access"]},
    "lifetime": {"name": "Lifetime", "price": 0, "limit": 999999, "features": ["Unlimited videos", "No watermark", "1080p", "Everything", "Owner access"]},
}

# ─── App ──────────────────────────────────────────────────────────────

app = FastAPI(title="ViralPulse", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "web" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "web" / "templates"))

# ─── Routes: Pages ────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = get_current_user(request.cookies.get("session"))
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "plans": PLANS})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_current_user(request.cookies.get("session"))
    if not user:
        return RedirectResponse("/login", status_code=302)
    
    conn = get_db()
    videos = conn.execute(
        "SELECT * FROM videos WHERE user_id = ? ORDER BY created_at DESC LIMIT 20",
        (user["id"],)
    ).fetchall()
    conn.close()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, "user": user, "videos": videos, "plans": PLANS
    })

@app.get("/billing", response_class=HTMLResponse)
async def billing_page(request: Request):
    user = get_current_user(request.cookies.get("session"))
    if not user:
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse("billing.html", {
        "request": request, "user": user, "plans": PLANS
    })

# ─── Routes: Auth API ─────────────────────────────────────────────────

@app.post("/api/register")
async def register(email: str = Form(...), password: str = Form(...), name: str = Form("")):
    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        raise HTTPException(400, "Email already registered")
    
    cursor = conn.execute(
        "INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)",
        (email, hash_password(password), name)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    token = create_session(user_id)
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie("session", token, httponly=True, max_age=30*24*3600)
    return response

@app.post("/api/login")
async def login(email: str = Form(...), password: str = Form(...)):
    conn = get_db()
    user = conn.execute(
        "SELECT id, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    
    if not user or user["password_hash"] != hash_password(password):
        raise HTTPException(401, "Invalid credentials")
    
    token = create_session(user["id"])
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie("session", token, httponly=True, max_age=30*24*3600)
    return response

@app.get("/api/logout")
async def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("session")
    return response

# ─── Routes: Video API ────────────────────────────────────────────────

@app.post("/api/generate")
async def generate_video(
    topic: str = Form(...),
    niche: str = Form("general"),
    user: dict = Depends(require_user)
):
    conn = get_db()
    
    # Check limits
    if user["videos_generated"] >= user["videos_limit"] and user["plan"] != "lifetime":
        conn.close()
        raise HTTPException(402, "Video limit reached. Please upgrade your plan.")
    
    # Create video record
    cursor = conn.execute(
        "INSERT INTO videos (user_id, topic, niche, status) VALUES (?, ?, ?, 'queued')",
        (user["id"], topic, niche)
    )
    video_id = cursor.lastrowid
    
    # Increment usage
    conn.execute(
        "UPDATE users SET videos_generated = videos_generated + 1, updated_at = datetime('now') WHERE id = ?",
        (user["id"],)
    )
    conn.commit()
    conn.close()
    
    # TODO: Queue video generation (for now, mark as pending)
    # In production, this would trigger a background job
    
    return {"status": "queued", "video_id": video_id, "message": "Video queued for generation"}

@app.get("/api/videos")
async def list_videos(user: dict = Depends(require_user)):
    conn = get_db()
    videos = conn.execute(
        "SELECT * FROM videos WHERE user_id = ? ORDER BY created_at DESC",
        (user["id"],)
    ).fetchall()
    conn.close()
    return [dict(v) for v in videos]

@app.get("/api/user")
async def get_user_info(user: dict = Depends(require_user)):
    plan = PLANS.get(user["plan"], PLANS["free"])
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "plan": user["plan"],
        "plan_name": plan["name"],
        "videos_generated": user["videos_generated"],
        "videos_limit": user["videos_limit"],
        "is_owner": bool(user["is_owner"]),
    }

# ─── Routes: Billing API ──────────────────────────────────────────────

@app.post("/api/billing/upgrade")
async def upgrade_plan(plan: str = Form(...), user: dict = Depends(require_user)):
    if plan not in PLANS:
        raise HTTPException(400, "Invalid plan")
    
    plan_info = PLANS[plan]
    conn = get_db()
    conn.execute(
        "UPDATE users SET plan = ?, videos_limit = ?, updated_at = datetime('now') WHERE id = ?",
        (plan, plan_info["limit"], user["id"])
    )
    conn.commit()
    conn.close()
    
    return {"status": "upgraded", "plan": plan, "limit": plan_info["limit"]}

# ─── Init ─────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    init_db()
    
    # Create owner account if doesn't exist
    conn = get_db()
    owner = conn.execute("SELECT id FROM users WHERE email = 'doug@viralpulse.com'").fetchone()
    if not owner:
        conn.execute(
            "INSERT INTO users (email, password_hash, name, plan, videos_limit, is_owner) VALUES (?, ?, ?, 'lifetime', 999999, 1)",
            ("doug@viralpulse.com", hash_password("viralpulse2026"), "Doug")
        )
        conn.commit()
        print("Owner account created: doug@viralpulse.com / viralpulse2026")
    conn.close()
