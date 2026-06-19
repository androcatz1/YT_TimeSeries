CREATE TABLE IF NOT EXISTS video_metrics_time_series (
    id BIGSERIAL PRIMARY KEY,

    video_id TEXT NOT NULL,
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