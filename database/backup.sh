#!/bin/bash
set -e

echo "📦 Starting backup..."

DATE=$(date -u +"%Y-%m-%d_%H-%M-%S")

pg_dump "$DATABASE_URL" \
  --no-owner \
  --no-acl \
  --schema=public \
  | gzip > "backup_$DATE.sql.gz"

echo "✅ Backup done: backup_$DATE.sql.gz"