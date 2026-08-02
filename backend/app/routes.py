from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserLogin, PostGenerateRequest, ScheduleRequest
from app.auth import get_current_user, verify_token
from app.services import openai, canva, social, firestore as fs
from firebase_admin import auth as firebase_auth
import asyncio
from datetime import datetime

router = APIRouter()

# ----------------- Auth -----------------
@router.post("/signup")
async def signup(user: UserCreate):
    try:
        # Create Firebase user
        user_record = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )
        # Store additional user data in Firestore
        fs.db.collection('users').document(user_record.uid).set({
            "email": user.email,
            "brand_name": user.brand_name,
            "brand_colors": user.brand_colors,
            "created_at": datetime.utcnow()
        })
        return {"uid": user_record.uid, "message": "User created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: UserLogin):
    # Firebase client SDK handles login on frontend; we just accept token via verify_token later.
    # We'll keep a simple endpoint to get custom token if needed.
    # For this demo, we'll return a message to use Firebase client SDK for login.
    return {"message": "Use Firebase client SDK to sign in, then send ID token in Authorization header"}

# ----------------- Content Generation -----------------
@router.post("/generate")
async def generate_posts(request: PostGenerateRequest, current_user = Depends(get_current_user)):
    uid = current_user['uid']
    brand = current_user['brand_name']
    colors = current_user['brand_colors']
    all_posts = []
    for platform in request.platforms:
        posts = await openai.generate_posts(brand, colors, request.themes, platform, request.count)
        for p in posts:
            post_data = {
                "caption": p['caption'],
                "hashtags": p['hashtags'],
                "category": p['category'],
                "platform": platform,
                "status": "draft",
                "image_url": None,
                "scheduled_time": None
            }
            post_id = fs.create_post(uid, post_data)
            all_posts.append({**post_data, "id": post_id})
    return {"posts": all_posts}

@router.post("/graphics/{post_id}")
async def generate_graphic(post_id: str, current_user = Depends(get_current_user)):
    uid = current_user['uid']
    post = fs.get_post(uid, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # Generate image using Canva
    image_url = await canva.create_graphic(post['caption'], current_user['brand_colors'])
    fs.update_post(uid, post_id, {"image_url": image_url})
    return {"image_url": image_url}

@router.post("/schedule")
async def schedule_posts(request: ScheduleRequest, current_user = Depends(get_current_user)):
    uid = current_user['uid']
    post = fs.get_post(uid, request.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    results = []
    for platform in request.platforms:
        if platform == "facebook":
            res = await social.post_to_facebook("page_id", post['caption'], post['image_url'], request.scheduled_time)
        elif platform == "instagram":
            res = await social.post_to_instagram("account_id", post['caption'], post['image_url'], request.scheduled_time)
        elif platform == "linkedin":
            res = await social.post_to_linkedin(post['caption'], post['image_url'], request.scheduled_time)
        else:
            continue
        results.append({platform: res})
    # Update post status and schedule time
    fs.update_post(uid, request.post_id, {
        "status": "scheduled",
        "scheduled_time": request.scheduled_time,
        "platforms": request.platforms
    })
    return {"scheduled": results}

@router.get("/posts")
async def list_posts(current_user = Depends(get_current_user)):
    posts = fs.get_user_posts(current_user['uid'])
    return {"posts": posts}