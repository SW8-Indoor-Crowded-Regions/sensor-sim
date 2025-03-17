from pydantic import BaseModel
from typing import List

class SensorModel(BaseModel):
  id: str
  rooms: List[str]
  movements: List[int]

class SensorListModel(BaseModel):
  sensors: List[SensorModel]

