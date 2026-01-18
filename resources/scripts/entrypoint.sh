#!/bin/bash
set -e

# echo "⏳ Running Alembic migrations..."
# alembic upgrade head

echo "🚀 Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000