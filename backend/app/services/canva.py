import requests
from app.config import settings

CANVA_API_BASE = "https://api.canva.com/v1"

async def create_graphic(text: str, brand_colors: str):
    # Real implementation would use Canva's design API.
    # For MVP, return a dummy image URL.
    return "https://via.placeholder.com/800x400/000000/FFFFFF?text=" + text.replace(" ", "+")