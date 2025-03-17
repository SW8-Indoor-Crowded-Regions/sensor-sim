from pydantic import BaseModel
from typing import List
from bson import ObjectId

class SensorModel(BaseModel):
	id: ObjectId
	rooms: List[ObjectId]
  
	def __str__(self):
		return f'Sensor (id={self.id}, rooms={self.rooms})'
 
	class Config:
		arbitrary_types_allowed = True
		json_encoders = {
			ObjectId: str,
		}
		  

class SensorListModel(BaseModel):
  sensors: List[SensorModel]

