# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PostRequest(BaseModel):
    days: int = 30
    categories: List[str] = ["product", "lifestyle", "tips"]
    platforms: List[str] = ["facebook", "instagram", "linkedin"]

class PostResponse(BaseModel):
    day: int
    category: str
    title: str
    preview: str
    time: str
    platforms: List[str]
    likes: int
    comments: int
    shares: int

class PostsResponse(BaseModel):
    posts: List[PostResponse]
    total: int
    user: str