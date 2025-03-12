from kafka import KafkaProducer
from dotenv import load_dotenv
import os
import json

def send_data(data: dict) -> None:
	"""Sends data to the Kafka broker."""
	load_dotenv()
	producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_BROKER"),
						value_serializer=lambda v: json.dumps(v).encode('utf-8'))
	producer.send("sensor-data", value=data)