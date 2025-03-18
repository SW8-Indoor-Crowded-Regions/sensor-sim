from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
import os
from typing import Callable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from app.classes.room import Room


class Consumer:
	def __init__(self, process_function: Callable[..., tuple[str, list["Room"]]], topic: str) -> None:
		load_dotenv()
		self.topic = topic
		self.broker = os.getenv('KAFKA_BROKER')
		self.process_function = process_function
		self.consumer = KafkaConsumer(
			self.topic,
			bootstrap_servers=self.broker,
			enable_auto_commit=True,
			value_deserializer=lambda v: json.loads(v.decode('utf-8')),
		)
		print(f"Connected to Kafka at {self.broker}, listening for messages on '{self.topic}'...")

	def consume_messages(self) -> None:
		"""Continuously listens for messages in the queue."""
		try:
			for message in self.consumer:
				self.process_function(message.value)
		except KeyboardInterrupt:  # pragma: no cover
			print('Consumer stopped.')
