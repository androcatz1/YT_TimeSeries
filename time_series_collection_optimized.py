import os
import csv
import time
import requests

from dotenv import load_dotenv
from datetime import datetime

# ==========================================================
# CONFIG
# ==========================================================

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

CHANNEL_IDS = [
    "UCpWvshQVx1d7BqCsPnVuNIw",
    "UCsWp7U58TZM8uOYtRrAqWhg",
    "UC2p8wkJVSjsMsRv0MjTikgA",
]

START_DATE = datetime(2026, 6, 15)

VIDEOS_CSV = "video_metadata_time_series.csv"

BASE_URL = "https://www.googleapis.com/youtube/v3"

THROTTLE = 0.5
MAX_QUOTA = 7000
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
    Reads existing CSV and builds:
    video_id -> platform
    """
    if not os.path.exists(VIDEOS_CSV):
        return {}

    known = {}

    with open(VIDEOS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vid = row.get("video_id")
            plat = row.get("platform")
            if vid and plat:
                known[vid] = plat

    print(f"Loaded {len(known)} cached platforms")
    return known


def detect_short(video_id):
    """
    Cheap heuristic via YouTube redirect behavior
    """
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
        "key": API_KEY,
    }

    r = requests.get(f"{BASE_URL}/channels", params=params)
    r.raise_for_status()

    quota_used += 1

    data = r.json()

    return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_ids_since_date(channel_id):
    """
    Fetch videos published >= START_DATE
    """
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
            "key": API_KEY,
        }

        r = requests.get(f"{BASE_URL}/playlistItems", params=params)
        r.raise_for_status()

        data = r.json()

        for item in data.get("items", []):

            snippet = item["snippet"]

            published_at = datetime.strptime(
                snippet["publishedAt"],
                "%Y-%m-%dT%H:%M:%SZ"
            )

            if published_at < START_DATE:
                stop = True
                break

            video_ids.append(snippet["resourceId"]["videoId"])

        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break

        time.sleep(THROTTLE)

    return video_ids


def fetch_video_metadata(video_ids, known_platforms):
    global quota_used

    fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    results = []

    for chunk in chunk_list(video_ids):

        if quota_used >= MAX_QUOTA:
            print("Quota limit reached.")
            break

        params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(chunk),
            "key": API_KEY,
        }

        r = requests.get(f"{BASE_URL}/videos", params=params)
        r.raise_for_status()

        quota_used += 1

        items = r.json().get("items", [])

        for video in items:

            snippet = video["snippet"]
            stats = video.get("statistics", {})
            video_id = video["id"]

            # ==================================================
            # PLATFORM (CACHED + ONLY NEW DETECTION)
            # ==================================================

            platform = known_platforms.get(video_id)

            if not platform:
                platform = detect_short(video_id)
                known_platforms[video_id] = platform
                print(f"Detected {video_id} -> {platform}")

            results.append({
                "video_id": video_id,
                "title": snippet["title"],
                "description": snippet.get("description", ""),
                "tags": snippet.get("tags", []),
                "category_id": snippet.get("categoryId", ""),
                "channel_title": snippet.get("channelTitle", ""),
                "published_at": snippet.get("publishedAt", ""),
                "views": stats.get("viewCount", "0"),
                "likes": stats.get("likeCount", "0"),
                "comments_count": stats.get("commentCount", "0"),
                "platform": platform,
                "fetched_at": fetch_time,
                "duration": video.get("contentDetails", {}).get("duration", "")
            })

        print(f"Fetched {len(items)} videos (quota: {quota_used})")

        time.sleep(THROTTLE)

    return results


def append_to_csv(rows):

    if not rows:
        return

    file_exists = os.path.isfile(VIDEOS_CSV)
    file_is_empty = (not file_exists) or os.path.getsize(VIDEOS_CSV) == 0

    with open(VIDEOS_CSV, "a", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=rows[0].keys())

        if file_is_empty:
            writer.writeheader()

        writer.writerows(rows)

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    known_platforms = load_known_platforms()

    all_video_ids = []

    for channel_id in CHANNEL_IDS:

        print(f"\nProcessing channel: {channel_id}")

        try:
            ids = get_video_ids_since_date(channel_id)

            print(
                f"Found {len(ids)} videos since {START_DATE.date()}"
            )

            all_video_ids.extend(ids)

        except Exception as e:
            print(f"Channel failed {channel_id}: {e}")

    # Remove duplicates (important)
    all_video_ids = list(set(all_video_ids))

    print(f"\nTotal unique videos: {len(all_video_ids)}")

    metadata = fetch_video_metadata(
        all_video_ids,
        known_platforms
    )

    append_to_csv(metadata)

    print(f"\nAppended {len(metadata)} rows")
    print(f"Total quota used: {quota_used}")