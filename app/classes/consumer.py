from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
import os
from typing import Callable

class Consumer:
		def __init__(self, process_function: Callable, topic: str):
				load_dotenv()
				self.topic = topic
				self.broker = os.getenv("KAFKA_BROKER")
				self.process_function = process_function
				self.consumer = KafkaConsumer(
						self.topic,
						bootstrap_servers=self.broker,
						enable_auto_commit=True,
						value_deserializer=lambda v: json.loads(v.decode('utf-8'))
				)
				print(f"Connected to Kafka at {self.broker}, listening for messages on '{self.topic}'...")

		def consume_messages(self):
				"""Continuously listens for messages in the queue."""
				try:
						for message in self.consumer:
								self.process_function(message.value)
				except KeyboardInterrupt:
						print("Consumer stopped.")

		def get_next_message(self, timeout=5):
				"""Fetch a single message with a timeout (default: 5 seconds)."""
				msg_pack = self.consumer.poll(timeout_ms=timeout * 1000)
				for tp, messages in msg_pack.items():
						for message in messages:
								return message.value  # Return the first message found
				return None  # Return None if no message is found