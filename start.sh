#!/bin/bash
set -e

# Wait for Kafka to be ready
/wait-for-it.sh kafka:9092 --timeout=30 -- echo "Kafka is up"

# Start the data processor in the background
python -m app.data_processor &

# Start the simulation in the background
python -m app.simulation &

# Start the API (in the foreground so Docker keeps the container running)
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

# Wait for background processes if needed
wait