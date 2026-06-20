import os
import time
import requests

from dotenv import load_dotenv
from datetime import datetime
from database.connection import get_connection
from config.settings import Settings
from zoneinfo import ZoneInfo

load_dotenv()
quota_used = 0

session = requests.Session()


# ==========================================================
# HELPERS
# ==========================================================

def chunk_list(lst, size=50):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def load_known_platforms():
    """
    Load latest known platform per video_id from DB
    (replaces CSV cache)
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT ON (video_id)
               video_id, platform
        FROM public.video_metrics_time_series
        ORDER BY video_id, fetched_at DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    known = {r[0]: r[1] for r in rows}

    print(f"Loaded {len(known)} cached platforms from DB")

    return known


def detect_short(video_id):
    url = f"https://www.youtube.com/shorts/{video_id}"

    try:
        resp = session.get(url, allow_redirects=True, timeout=10)

        if "/shorts/" in resp.url:
            return "Short"
        return "Regular"

    except requests.RequestException:
        return "Unknown"


def get_uploads_playlist(channel_id):
    global quota_used

    params = {
        "part": "contentDetails",
        "id": channel_id,
        "key": Settings.YOUTUBE_API_KEY,
    }

    r = requests.get(f"{Settings.BASE_URL}/channels", params=params)
    r.raise_for_status()

    quota_used += 1

    return r.json()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_ids_since_date(channel_id):

    uploads_playlist = get_uploads_playlist(channel_id)

    video_ids = []
    next_page_token = None
    stop = False

    while not stop:

        params = {
            "part": "snippet",
            "playlistId": uploads_playlist,
            "maxResults": 50,
            "pageToken": next_page_token,
            "key": Settings.YOUTUBE_API_KEY,
        }

        r = requests.get(f"{Settings.BASE_URL}/playlistItems", params=params)
        r.raise_for_status()

        data = r.json()

        for item in data.get("items", []):

            snippet = item["snippet"]

            published_at = datetime.strptime(
                snippet["publishedAt"],
                "%Y-%m-%dT%H:%M:%SZ"
            )

            if published_at < Settings.START_DATE:
                stop = True
                break

            video_ids.append(snippet["resourceId"]["videoId"])

        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break

        time.sleep(Settings.THROTTLE)

    return video_ids


def fetch_video_metadata(video_ids, known_platforms):
    global quota_used

    fetch_time = datetime.now()

    results = []

    for chunk in chunk_list(video_ids):

        if quota_used >=Settings.MAX_QUOTA:
            print("Quota limit reached.")
            break

        params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(chunk),
            "key": Settings.YOUTUBE_API_KEY,
        }

        r = requests.get(f"{Settings.BASE_URL}/videos", params=params)
        r.raise_for_status()

        quota_used += 1

        items = r.json().get("items", [])

        for video in items:

            snippet = video["snippet"]
            stats = video.get("statistics", {})
            video_id = video["id"]

            # PLATFORM LOGIC (cached + detect once)
            platform = known_platforms.get(video_id)

            if not platform:
                platform = detect_short(video_id)
                known_platforms[video_id] = platform
                print(f"Detected {video_id} -> {platform}")

            published_at = snippet.get("publishedAt", "") 

            results.append((
                video_id,
                snippet["title"],
                snippet.get("description", ""),
                str(snippet.get("tags", [])),
                snippet.get("categoryId", ""),
                snippet.get("channelTitle", ""),
                published_at,
                int(stats.get("viewCount", 0)),
                int(stats.get("likeCount", 0)),
                int(stats.get("commentCount", 0)),
                platform,
                fetch_time,
                video.get("contentDetails", {}).get("duration", "")
            ))

        print(f"Fetched {len(items)} videos (quota: {quota_used})")

        time.sleep(Settings.THROTTLE)

    return results