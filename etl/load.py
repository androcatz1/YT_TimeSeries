import psycopg2
from psycopg2.extras import execute_values
from database.connection import get_connection


def insert_to_postgres(rows):

    if not rows:
        return

    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO public.video_metrics_time_series (
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
            fetched_at,
            duration
        ) VALUES %s
    """

    execute_values(cur, query, rows, page_size=5000)

    conn.commit()
    cur.close()
    conn.close()