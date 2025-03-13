class Room ():
	"""Represents a room in a building."""
	from .sensor import Sensor
	def __init__(self, room_info: dict, crowd_factor: float, area: float, sensors: list[Sensor]):
		self.id = room_info["id"]
		self.name = room_info["name"]
		self.type = room_info["type"]
		self.occupancy = 0
		self.crowd_factor = crowd_factor
		self.area = area
		self.sensors = sensors
	
	def add_occupants(self, occupants: int) -> None:
		"""Increments the room's occupancy by the number of occupants.

		Args:
				occupants (int): The number of occupants to add to the room's occupancy.
		"""
		self.occupancy += occupants
	
	def remove_occupants(self, occupants: int) -> None:
		"""Decrements the room's occupancy by the number of occupants given.

		Raises:
				Exception: If the room's occupancy woulde be less than zero.
		"""
		if self.occupancy - occupants < 0:
			raise Exception("Room occupancy cannot be less than zero. The room is empty.")
		self.occupancy -= occupants

	def __str__(self) -> str:
		return f"Room (id={self.id}, name={self.name}, type={self.type}, occupancy={self.occupancy}, crowdFactor={self.crowd_factor}, area={self.area}, sensors={['Sensor id: ' + sensor.id.__str__() for sensor in self.sensors]})"