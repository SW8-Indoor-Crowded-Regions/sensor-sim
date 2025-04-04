from pydantic import BaseModel, field_serializer, model_validator, Field
from typing import Union
from typing import List
from bson import ObjectId, DBRef

class SensorModel(BaseModel):
	id: Union[str, ObjectId] = Field(alias="id")
	rooms: List[Union[str, DBRef]]
	latitude: float
	longitude: float
	model_config = {"arbitrary_types_allowed": True}

	@model_validator(mode="before")
	def convert_fields(cls, values):
		"""Convert fields to correct types before validation."""
		values["rooms"] = [str(room.id) if isinstance(room, DBRef) else str(room) for room in values["rooms"]]
		return values

	@field_serializer("id")
	def serialize_id(self, id, _info):
		return str(id)

	@field_serializer("rooms")
	def serialize_rooms(self, rooms, _info):
		return [str(room) for room in rooms]
		  

class SensorListModel(BaseModel):
  sensors: List[SensorModel]

