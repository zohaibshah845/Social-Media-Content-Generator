import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CANVA_ACCESS_TOKEN = os.getenv("CANVA_ACCESS_TOKEN")
    FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this_in_production")

settings = Settings()