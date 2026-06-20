import os
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

    MAX_RESULTS = 50
    REQUEST_TIMEOUT = 30

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    START_DATE = datetime(2026, 6, 15)

    THROTTLE = 0.5
    MAX_QUOTA = 7000

    CHANNEL_IDS = [
        "UCpWvshQVx1d7BqCsPnVuNIw",
        "UCsWp7U58TZM8uOYtRrAqWhg",
        "UC2p8wkJVSjsMsRv0MjTikgA",
    ]
