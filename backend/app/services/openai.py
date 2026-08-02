import openai
import json
from app.config import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_posts(brand_name: str, brand_colors: str, themes: list, platform: str, count: int = 30):
    prompt = f"""
    You are an expert social media strategist. Generate {count} posts for {platform} for the brand "{brand_name}" with brand colors {brand_colors}.
    Themes: {', '.join(themes)}.
    Each post must have:
    - caption (engaging, 100-200 words, with emojis)
    - 5 relevant hashtags
    - content category (e.g., educational, promotional, inspirational)
    Return a JSON array of objects with keys: caption, hashtags, category.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content)
    # data might be {"posts": [...]} or directly list
    if isinstance(data, dict) and "posts" in data:
        return data["posts"]
    return data  # assume list