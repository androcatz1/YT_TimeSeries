from database.connection import get_connection

SCHEMA = """
CREATE TABLE IF NOT EXISTS video_metrics_time_series (
    id BIGSERIAL PRIMARY KEY,
    video_id TEXT,
    title TEXT,
    description TEXT,
    tags TEXT,
    category_id TEXT,
    channel_title TEXT,
    published_at TIMESTAMP,
    views BIGINT,
    likes BIGINT,
    comments_count BIGINT,
    platform TEXT,
    fetched_at TIMESTAMP(0),
    duration TEXT
);
"""


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(SCHEMA)

    conn.commit()
    cursor.close()
    conn.close()

    print("Database initialized ✅")


if __name__ == "__main__":
    init_db()