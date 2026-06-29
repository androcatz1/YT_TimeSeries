from etl.extract import (
    load_known_platforms,
    get_video_ids_since_date,
    fetch_video_metadata,
    load_known_topics
)
from etl.transform import transform, label_topic
from etl.load import insert_to_postgres
from config.settings import Settings
import pandas as pd

if __name__ == "__main__":
    known_platforms = load_known_platforms()
    known_topics = load_known_topics()

    all_video_ids = []

    for channel_id in Settings.CHANNEL_IDS:
        ids = get_video_ids_since_date(channel_id)
        all_video_ids.extend(ids)

    rows = fetch_video_metadata(
        all_video_ids,
        known_platforms,
        known_topics
    )

    df = transform(rows)
    df_labelled = label_topic(df)

    rows_transformed = list(df_labelled.to_records(index = False))
    insert_to_postgres(rows_transformed)