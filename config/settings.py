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

    COLUMNS_RAW = [
        "video_id", "title", "description", "tags", "category_id", 
        "channel_title", "published_at", "views", "likes", 
        "comments_count", "platform", "topic", "fetched_at", "duration"
    ]

    TAGS_TO_REMOVE = {'news', 'the star tv', 'thestartv','the star','nstonline', 'nst', 'new straits times', 'bth', 
                      '#beyondtheheadlines', 'nst sport','bu', 'buletin tv3', 'buletin utama', 'buletintv3', 'butv3', 
                      'buletin malaysia', 'berita malaysia', 'berita terkini','trending', 'malaysia', 'tv3', 'buletin tv9', 
                      'ntv7', '8tv', 'tonton', 'astro awani', 'berita rtm', 'berita malaysia', 'news Malaysia', 'malay news', 
                      'news', 'malay', 'berita', 'nst education', 'nst news', 'nst groove', 'nst beyond the headlines', 
                      'nst sea games coverage', 'berita semasa', 'berita terkini', 'perkembangan semasa','buletin malaysia', 
                      'berita malaysia', 'tonton', 'ntv7', '8tv', 'astro awani', 'berita rtm', 'berita tv9', 'news malaysia',
                      'news malay', 'news mpb', 'trending nombor 1', 'trending', 'trending worldwide'}
    


class Gemini:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_ID = "gemini-3.1-flash-lite"
    BATCH_SIZE = 10

    SYSTEM_PROMPT = """You are a topic classifier for Malaysian news content.
    Text may be in English, Malay, or a mix of both (code-switching is common).
    You will be given a news article title.

    Reply ONLY with the topic name.
    """
    USER_PROMPT_TEMPLATE = """Classify each Malaysian news title into EXACTLY ONE topic.

    TOPICS:
    - Politics
    - Crime & Law
    - Accident & Disaster
    - Economy & Business
    - Sports
    - Health & Medicine
    - Education
    - Technology
    - Environment
    - Social & Community
    - International
    - Entertainment & Lifestyle
    - Military & Defence
    - Transportation & Infrastructure
    - Weather & Climate
    - Other

    DECISION RULES:
    1. If the title contains a known Malaysian politics keyword (PRN, DUN, Dewan Rakyat, PN, PH, BN, parti) → Politics
    2. Mahkamah / court / didakwa / charged → Crime & Law
    3. Kemalangan / nahas / maut in accident context → Accident & Disaster
    4. Perang / war / konflik / Israel / Iran / Ukraine / Russia in foreign context → International
    5. Date-only titles or show names (Nightline, News@9, Market Pulse, Buletin Pagi) → Other
    6. If unsure between Politics and Crime, prosecution always → Crime & Law

    Return ONE topic per line, in the SAME ORDER as the titles, but DO NOT include the numbering.

    Titles:
    {titles}
    """