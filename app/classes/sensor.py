from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.classes.room import Room

class Sensor ():
	def __init__(self, id: int, rooms: list["Room"]):
		self.id = id
		self.rooms = rooms
		self.movements = [0, 0]

	def pass_sensor(self, from_room: int) -> "Room":
		"""Checks if the from_room ID matches the first or second room in the rooms tuple."""
		if from_room == self.rooms[0].id:
			direction = 1
		elif from_room == self.rooms[1].id:
			direction = 0
		else:
			raise Exception("No room found with id:", from_room)
		self.movements[direction] += 1
		return self.rooms[direction]
	
	def __str__(self) -> str:
		return f"Sensor(id={self.id}, rooms={['Room id: ' + room.id.__str__() for room in self.rooms]}, movements={self.movements})"