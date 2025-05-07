#!/bin/bash
set -e

# Wait for Kafka to be fully ready (TCP port + protocol handshake)
echo "⌛ Waiting for Kafka broker to be ready..."
python -c '
import time
from kafka import KafkaAdminClient
for i in range(30):
    try:
        admin = KafkaAdminClient(bootstrap_servers="kafka:9092", client_id="check")
        admin.list_topics()
        print("✅ Kafka broker is ready.")
        break
    except Exception as e:
        print(f"Kafka not ready yet: {e}")
        time.sleep(2)
else:
    raise RuntimeError("Kafka broker was not ready in time.")
'

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
