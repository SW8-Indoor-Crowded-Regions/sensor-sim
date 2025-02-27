from kafka import KafkaProducer
import json
import time
import random

# Kafka setup
KAFKA_TOPIC = "sensor-data"
KAFKA_BROKER = "kafka:9092"

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Simulating multiple sensors
SENSOR_IDS = ["room_101", "room_102", "room_103"]

def generate_sensor_data(sensor_id):
    """Simulates sensor data with realistic crowd movement patterns."""
    return {
        "sensor_id": sensor_id,
        "timestamp": time.time(),
        "people_count": max(0, int(random.gauss(10, 3)))  # Gaussian distribution around 10 people
    }

while True:
    for sensor_id in SENSOR_IDS:
        sensor_data = generate_sensor_data(sensor_id)
        producer.send(KAFKA_TOPIC, value=sensor_data)
        print(f"Sent: {sensor_data}")
    time.sleep(1)  # Simulate 1-second interval