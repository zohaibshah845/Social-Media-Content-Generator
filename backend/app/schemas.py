from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    brand_name: str
    brand_colors: Optional[str] = "#000000,#FFFFFF"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostGenerateRequest(BaseModel):
    themes: List[str]
    platforms: List[str]  # e.g. ["facebook", "instagram", "linkedin"]
    count: int = 30

class PostResponse(BaseModel):
    id: str
    caption: str
    hashtags: List[str]
    category: str
    image_url: Optional[str]
    scheduled_time: Optional[datetime]
    platforms: List[str]
    status: str  # draft, scheduled, published, failed

class ScheduleRequest(BaseModel):
    post_id: str
    platforms: List[str]
    scheduled_time: datetime