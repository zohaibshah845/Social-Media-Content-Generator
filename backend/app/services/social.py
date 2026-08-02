import requests
from app.config import settings
from datetime import datetime

async def post_to_facebook(page_id: str, message: str, image_url: str, scheduled_time: datetime):
    # Actual implementation using Facebook Graph API
    return {"status": "scheduled", "id": "mock_fb_id"}

async def post_to_instagram(account_id: str, message: str, image_url: str, scheduled_time: datetime):
    return {"status": "scheduled", "id": "mock_ig_id"}

async def post_to_linkedin(message: str, image_url: str, scheduled_time: datetime):
    return {"status": "scheduled", "id": "mock_li_id"}