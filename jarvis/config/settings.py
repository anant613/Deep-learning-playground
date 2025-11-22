import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Voice Settings
    WAKE_WORD = "jarvis"
    VOICE_RATE = 200
    VOICE_VOLUME = 0.9
    
    # Server Settings
    HOST = "127.0.0.1"
    PORT = 8000
    
    # Database
    DATABASE_PATH = "jarvis.db"
    
    # Free Services URLs
    WEATHER_BASE_URL = "https://wttr.in"  # Free weather service
    NEWS_RSS_FEEDS = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.reuters.com/reuters/topNews"
    ]
    
    # AI Model Settings
    AI_MODEL_NAME = "microsoft/DialoGPT-medium"  # Free local model
    USE_LOCAL_AI = True

settings = Settings()