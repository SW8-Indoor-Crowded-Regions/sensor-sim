import bson.errors
from fastapi import HTTPException
from db.models.sensor import Sensor
from app.utils.data_models.sensors import SensorModel
import bson
import traceback

async def get_all_sensors() -> list[SensorModel]:
	"""Fetch all sensors from the database."""
	try:
		sensors = Sensor.objects().no_dereference()  # type: ignore
		return sensors
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
  
async def get_sensor_by_id(sensor_id: str) -> SensorModel:
	"""Fetch a sensor by its id."""
	validate_sensor_id(sensor_id)
	try:
		sensor = Sensor.objects(id=bson.ObjectId(sensor_id)).no_dereference().first() # type: ignore
	except Exception as e:
		traceback.print_exc()
		raise HTTPException(status_code=500, detail=str(e))
	if not sensor:
		raise HTTPException(status_code=404, detail='Sensor not found.')
	return sensor
  
def validate_sensor_id(sensor_id: str):
  if not bson.ObjectId.is_valid(sensor_id):
    raise HTTPException(status_code=400, detail='Invalid sensor id.')