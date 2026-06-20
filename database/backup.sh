#!/bin/bash
set -e

echo "📦 Starting backup..."

DATE=$(date -u +"%Y-%m-%d")

docker run --rm postgres:17 \
  pg_dump "$DATABASE_URL" \
  --no-owner \
  --no-acl \
  --schema=public \
  | gzip > backup_$DATE.sql.gz

echo "✅ Backup done: backup_$DATE.sql.gz"