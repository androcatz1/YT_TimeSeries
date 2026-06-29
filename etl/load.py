import psycopg2
from psycopg2.extras import execute_values
from database.connection import get_connection


def insert_to_postgres(rows):

    if not rows:
        return

    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO video_metrics_time_series_transformed (
        video_id,
        title,
        description,
        tags,
        category_id,
        channel_title,
        published_at,
        views,
        likes,
        comments_count,
        platform,
        topic,
        fetched_at,
        duration,
        published_hour,
        published_day,
        published_month,
        duration_mins,
        engagement_rate,
        duration_bucket,
        days_since_published 
    ) VALUES %s
"""

    execute_values(cur, query, rows, page_size=5000)

    conn.commit()
    cur.close()
    conn.close()