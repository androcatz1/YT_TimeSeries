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