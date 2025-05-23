from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from app.classes.sensor import Sensor


class Room:
	"""Represents a room in a building."""

	def __init__(
		self,
		room_info: dict,
		crowd_factor: float,
		popularity_factor: float,
		area: float,
		sensors: list['Sensor'],
	):
		self.id: int = room_info['id']
		self.name: str = room_info['name']
		self.type: str = room_info['type']
		self.occupancy: int = 0
		self.crowd_factor: float = crowd_factor
		self.popularity_factor: float = popularity_factor
		self.area: float = area
		self.sensors: list['Sensor'] = sensors

	def add_occupants(self, occupants: int) -> None:
		"""Increments the room's occupancy by the number of occupants.
		Args:
		occupants (int): The number of occupants to add to the room's occupancy.
		"""
		if occupants <= 0:
			return
		self.occupancy += occupants

	def remove_occupants(self, occupants: int) -> None:
		"""Decrements the room's occupancy by the number of occupants,ensuring it never goes below zero."""
		if occupants <= 0:
			return
		actual_removed = min(occupants, self.occupancy)
		self.occupancy -= actual_removed

	def __str__(self) -> str:
		return f'Room (id={self.id}, name={self.name}, type={self.type}, occupancy={self.occupancy}, crowdFactor={self.crowd_factor}, popularityFactor={self.popularity_factor}, area={self.area}, sensors={["Sensor id: " + sensor.id.__str__() for sensor in self.sensors]})'
