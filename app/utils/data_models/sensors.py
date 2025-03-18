from pydantic import BaseModel, field_serializer
from typing import List
from bson import ObjectId, DBRef

class SensorModel(BaseModel):
	id: ObjectId
	rooms: List[DBRef]
	model_config = {
        "arbitrary_types_allowed": True
    }
 
	def __init__(self, id, rooms):
		id = ObjectId(id)
		rooms = [DBRef('rooms', room) for room in rooms]
		super().__init__(id=id, rooms=rooms)

	@field_serializer('id')
	def serialize_id(self, id, _info):
		return str(id)

	@field_serializer('rooms')
	def serialize_rooms(self, rooms, _info):
		return [str(room.id) for room in rooms]
		  

class SensorListModel(BaseModel):
  sensors: List[SensorModel]

