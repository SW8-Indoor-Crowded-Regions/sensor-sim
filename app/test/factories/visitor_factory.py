import bson
from app.classes.visitor import Visitor
from app.test.factories.room_factory import RoomFactory
from app.utils.heuristics import MovementConfig


class VisitorFactory:
	def __init__(
		self,
		id: int = None,
		rooms: list = None,
		popularity_factor: float = 1.0,
		area: float = 100.0,
		config: MovementConfig = None
	):
		self.id = id or bson.ObjectId()
		self.rooms = rooms or [RoomFactory(popularity_factor=popularity_factor, area=area)]
		self.config = config or MovementConfig(alpha=0.5, beta=0.5, penalty_factor=0.5, create_visitor_probability=0.5)

	def create(self) -> Visitor:
		"""Create a Visitor instance with the specified configuration."""
		return Visitor(id=self.id, rooms=self.rooms, config=self.config)

	def __call__(self, **kwargs):
		"""Allows the factory instance to be called like a function."""
		return VisitorFactory(**kwargs)

