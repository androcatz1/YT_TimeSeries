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

SCHEMA_TRANSFORMED= """
CREATE TABLE IF NOT EXISTS video_metrics_time_series_transformed (
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
    topic TEXT,
    fetched_at TIMESTAMP(0),
    duration TEXT,
    published_hour INT,
    published_day VARCHAR(9),
    published_month VARCHAR(9),
    duration_mins DOUBLE PRECISION,
    engagement_rate DOUBLE PRECISION,
    duration_bucket TEXT,
    days_since_published INT
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