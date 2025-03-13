from pydantic import BaseModel
from typing import List


class RoomModel(BaseModel):
	_id: str
	name: str
	type: str
	crowd_factor: float
	area: float
	longitude: float
	latitude: float


class RoomListModel(BaseModel):
	rooms: List[RoomModel]
