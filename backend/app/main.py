from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(title="Social Content Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}

# NEW: Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Social Content Generator API"}