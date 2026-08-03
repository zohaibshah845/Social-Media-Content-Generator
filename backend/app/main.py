import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

# Load environment variables from .env file
load_dotenv()

# Optional: print loaded keys (for debugging) – remove in production
print("✅ OPENAI_API_KEY         =", os.getenv("OPENAI_API_KEY", "NOT SET")[:20] + "..." if os.getenv("OPENAI_API_KEY") else "❌ NOT SET")
print("✅ FIREBASE_CREDENTIALS_PATH =", os.getenv("FIREBASE_CREDENTIALS_PATH", "NOT SET"))
print("✅ CANVA_CLIENT_ID        =", os.getenv("CANVA_CLIENT_ID", "NOT SET")[:10] + "..." if os.getenv("CANVA_CLIENT_ID") else "❌ NOT SET")

app = FastAPI(
    title="Social Content Generator API",
    description="Generate content for social media using AI and external services.",
    version="1.0.0",
)

# CORS – allow all origins for development, restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use ["https://your-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes from routes.py under /api/v1
app.include_router(router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Social Content Generator API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0",
    }

# Health check
@app.get("/health")
async def health():
    # Optionally check if Firebase is initialized, OpenAI key is present, etc.
    firebase_ok = os.path.exists(os.getenv("FIREBASE_CREDENTIALS_PATH", ""))
    openai_ok = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "status": "ok",
        "firebase_credentials_exist": firebase_ok,
        "openai_key_set": openai_ok,
    }

# (Optional) Development endpoint to see config – remove in production!
@app.get("/debug/config")
async def debug_config():
    return {
        "FIREBASE_CREDENTIALS_PATH": os.getenv("FIREBASE_CREDENTIALS_PATH"),
        "OPENAI_API_KEY_SET": bool(os.getenv("OPENAI_API_KEY")),
        "CANVA_CLIENT_ID_SET": bool(os.getenv("CANVA_CLIENT_ID")),
        "SECRET_KEY_SET": bool(os.getenv("SECRET_KEY")),
        # Do NOT expose full keys!
    }