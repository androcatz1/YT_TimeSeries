from etl.extract import (
    load_known_platforms,
    get_video_ids_since_date,
    fetch_video_metadata
)
from config.settings import Settings
from etl.load import insert_to_postgres

if __name__ == "__main__":
    known_platforms = load_known_platforms()

    all_video_ids = []

    for channel_id in Settings.CHANNEL_IDS:
        ids = get_video_ids_since_date(channel_id)
        all_video_ids.extend(ids)

    rows = fetch_video_metadata(
        all_video_ids,
        known_platforms
    )

    insert_to_postgres(rows)