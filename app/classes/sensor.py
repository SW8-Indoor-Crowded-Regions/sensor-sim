from dotenv import load_dotenv
import os
from kafka import KafkaProducer
import json

class Sensor ():
	def __init__(self, id: int, rooms: list):
		self.id = id
		self.rooms = rooms
		self.movements = [0, 0]
	
	def send_data(self):
		"""Sends data to the Kafka broker."""
		load_dotenv()
		producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_BROKER"),
						 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
		producer.send("sensor-data", value=self.movements)

	def pass_sensor(self, from_room: int):
		"""Checks if the from_room ID matches the first or second room in the rooms tuple."""
		if from_room == self.rooms[0].id:
			direction = 0
		elif from_room == self.rooms[1].id:
			direction = 1
		else:
			raise Exception("No room found with id:", from_room)
 
		self.movements[direction] += 1
	
	def __str__(self) -> str:
		return f"Sensor(id={self.id}, rooms={[room.id for room in self.rooms]}, movements={self.movements})"
		
		
	"""
if __name__ == "__main__":
	from room import Room
	sensor = Sensor(1, [
  	Room({"id": 1, "name": "101", "type": "lounge"}, 1.5, 101.2, []), 
		Room({"id": 2, "name": "102", "type": "exhibition"}, 1.2, 111.2, [])])
	sensor.pass_sensor(1)
	sensor.pass_sensor(2)
	sensor.send_data()
 
 """