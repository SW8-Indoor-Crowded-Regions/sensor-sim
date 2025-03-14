from kafka import KafkaConsumer
import json

# Kafka setup
KAFKA_TOPIC = 'sensor-data'
KAFKA_BROKER = 'localhost:9092'

consumer = KafkaConsumer(
	KAFKA_TOPIC,
	bootstrap_servers=KAFKA_BROKER,
	enable_auto_commit=True,
	value_deserializer=lambda v: json.loads(v.decode('utf-8')),
)

print(f"Connected to Kafka at {KAFKA_BROKER}, listening for messages on '{KAFKA_TOPIC}'...\n")

for message in consumer:
	print(f'Received: {message.value}')
