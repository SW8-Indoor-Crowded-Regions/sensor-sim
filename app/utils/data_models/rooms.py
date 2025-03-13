from pydantic import BaseModel
from typing import List
from bson import ObjectId


class RoomModel(BaseModel):
	id: str
	name: str
	type: str
	crowd_factor: float
	area: float
	longitude: float
	latitude: float

class RoomListModel(BaseModel):
	rooms: List[RoomModel]
