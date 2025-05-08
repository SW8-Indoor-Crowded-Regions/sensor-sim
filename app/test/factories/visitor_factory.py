import bson
from app.classes.visitor import Visitor
from app.test.factories.room_factory import RoomFactory


class VisitorFactory:
	def __init__(
		self,
		id: int = None,
		rooms: list = None,
		popularity_factor: float = 1.0,
		area: float = 100.0,
	):
		self.id = id or bson.ObjectId()
		self.rooms = rooms or [RoomFactory(popularity_factor=popularity_factor, area=area)]

	def create(self) -> Visitor:
		"""Create a Visitor instance with the specified configuration."""
		return Visitor(id=self.id, rooms=self.rooms)

	def __call__(self, **kwargs):
		"""Allows the factory instance to be called like a function."""
		return VisitorFactory(**kwargs)

