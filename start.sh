#!/bin/bash
set -e

# Populate MongoDB (initial data)
echo "📦 Populating MongoDB..."
python -m populate

# Start data processor
echo "📡 Starting data processor..."
python -m app.data_processor &

# Give it a moment to set up any consumers/producers
sleep 2

# Start simulation
echo "📈 Starting simulation..."
python -m app.simulation &

# Start API in foreground
echo "🚀 Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
