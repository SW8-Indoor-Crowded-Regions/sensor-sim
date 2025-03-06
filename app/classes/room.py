class Room ():
	"""Represents a room in a building."""
	from .sensor import Sensor
	def __init__(self, room_info, crowd_factor: float, area: float, sensors: list[Sensor]):
		self.id = room_info["id"]
		self.name = room_info["name"]
		self.type = room_info["type"]
		self.occupancy = 0
		self.crowd_factor = crowd_factor
		self.area = area
		self.sensors = sensors
	
	def increment_occupancy(self):
		"""Increments the room's occupancy by one."""
		self.occupancy += 1
	
	def decrement_occupancy(self):
		"""Decrements the room's occupancy by one.

		Raises:
				Exception: If the room's occupancy woulde be less than zero.
		"""
		if self.occupancy < 0:
			raise Exception("Room occupancy cannot be less than zero. The room is empty.")
		self.occupancy -= 1
