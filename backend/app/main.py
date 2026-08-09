from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router
from .routes import router as posts_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Content Generator API",
    description="Generate 30 days of content for social media",
    version="1.0.0"
)

# ===== CORS Configuration - FIXED =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
    expose_headers=["Content-Type", "Authorization"],
)

# ===== Routes =====
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(posts_router, prefix="/posts", tags=["Posts"])

@app.get("/")
async def root():
    return {"message": "Content Generator API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)