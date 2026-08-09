from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random
from datetime import datetime
from .auth import get_current_user

router = APIRouter()

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

# Post templates
POST_TEMPLATES = {
    "product": [
        {"title": "🚀 Product Spotlight", "preview": "Discover how our new feature saves teams 2 hours daily. Try it now!"},
        {"title": "📦 New Integration", "preview": "We just added Slack + Teams support. Work smarter, not harder."},
        {"title": "📊 Analytics Insight", "preview": "The one metric that actually predicts growth."},
        {"title": "📈 Growth Strategy", "preview": "The simple framework that helped us 2x our user base."},
        {"title": "✨ Feature Highlight", "preview": "Our most requested feature is finally here. Check it out!"},
        {"title": "🔔 Product Alert", "preview": "New update rolling out next week. Here's what's changing."},
    ],
    "lifestyle": [
        {"title": "🧘 Morning Routine", "preview": "5 simple habits that transformed my productivity and focus."},
        {"title": "🌿 Work-Life Balance", "preview": "Setting boundaries isn't selfish. Here's how I protect my time."},
        {"title": "🎯 Q3 Goals", "preview": "How to set achievable goals that actually get done."},
        {"title": "🌱 Daily Habits", "preview": "Small changes that lead to big results over time."},
        {"title": "🧠 Mental Wellness", "preview": "Taking care of your mind is just as important as your body."},
    ],
    "tips": [
        {"title": "💡 Quick Win", "preview": "This keyboard shortcut alone saves me 30 minutes every day."},
        {"title": "🔧 Automation Hack", "preview": "Automate 3 repetitive tasks and reclaim your week."},
        {"title": "🤝 Team Sync", "preview": "5 tips for better remote collaboration and fewer meetings."},
        {"title": "⚡ Productivity Tip", "preview": "Work in 90-minute focused sprints for maximum output."},
    ]
}

@router.post("/generate-posts")
async def generate_posts(
    request: PostRequest,
    current_user = Depends(get_current_user)
):
    """Generate 30 days of posts for the authenticated user"""
    posts = []
    platforms = ["facebook", "instagram", "linkedin"]
    
    for i in range(1, request.days + 1):
        # Select category
        category = random.choice(request.categories)
        templates = POST_TEMPLATES.get(category, POST_TEMPLATES["tips"])
        template = random.choice(templates)
        
        # Random time
        hour = random.randint(1, 12)
        minute = random.randint(0, 59)
        ampm = "AM" if random.random() > 0.5 else "PM"
        time_str = f"{hour}:{str(minute).zfill(2)} {ampm}"
        
        # Random platforms
        num_platforms = random.randint(1, 3)
        used_platforms = random.sample(platforms, num_platforms)
        
        # Engagement metrics
        likes = random.randint(10, 210)
        comments = random.randint(1, 30)
        shares = random.randint(1, 20)
        
        posts.append({
            "day": i,
            "category": category.capitalize(),
            "title": template["title"],
            "preview": template["preview"],
            "time": time_str,
            "platforms": used_platforms,
            "likes": likes,
            "comments": comments,
            "shares": shares
        })
    
    return {
        "posts": posts,
        "total": len(posts),
        "user": current_user["email"]
    }

@router.get("/posts")
async def get_posts(current_user = Depends(get_current_user)):
    """Get saved posts for the current user"""
    return {
        "posts": [],
        "message": "No saved posts found"
    }