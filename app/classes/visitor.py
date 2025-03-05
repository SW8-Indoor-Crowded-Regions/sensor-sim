from app.classes.room import Room
from app.classes.sensor import Sensor

class Visitor():
	def __init__(self, id: int, rooms: list["Room"]):
		self.id = id
		self.visited_rooms = rooms

	def get_current_room(self) -> Room:
		"""Returns the room that the visitor is currently in.

		Returns:
				Room: The room that the visitor is currently in.
		"""
		return self.visited_rooms[-1]
		
	def get_movement_options(self) -> list[Sensor]:
		"""Returns the sensors that the visitor can move to.

		Returns:
				list[Sensor]: The sensors that the visitor can move to.
		"""
		# Return all sensors in room sensors for each room self.visited_rooms
		return [sensor for sensor in self.get_current_room().sensors]
	
	def move(self, sensor: Sensor):
		"""Moves the visitor to the room connected to the sensor.

		Args:
				sensor (Sensor): The sensor (/door) that the visitor will move through.
		"""
		room = sensor.pass_sensor(self.get_current_room().id)
		self.visited_rooms.append(room)

	def __str__(self) -> str:
	 return f"Visitor (id={self.id}, visitedRooms={[room.id for room in self.visited_rooms]})"