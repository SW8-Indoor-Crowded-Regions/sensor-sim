import bson.errors
from fastapi import HTTPException
from db.models.sensor import Sensor
from app.utils.data_models.sensors import SensorModel
import bson

async def get_all_sensors() -> list[SensorModel]:
  """Fetch all sensors from the database."""
  try:
    sensors = Sensor.objects()  # type: ignore
    serialized_sensors = []

    for sensor in sensors:
      serialized_sensors.append({ # pragma: no cover
        "id": str(sensor.id),
        "name": sensor.name,
        "rooms": [str(room.id) for room in sensor.rooms],
        "movements": sensor.movements
      })

    return serialized_sensors
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
async def get_sensor_by_id(sensor_id: str) -> SensorModel:
  """Fetch a sensor by its id."""
  validate_sensor_id(sensor_id)
  try:
    sensor = await fetch_sensor_by_id(sensor_id)
    return sensor
  except HTTPException:
    raise
  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail=str(e))
  
def validate_sensor_id(sensor_id: str):
  if not bson.ObjectId.is_valid(sensor_id):
    raise HTTPException(status_code=400, detail='Invalid sensor id.')
  
async def fetch_sensor_by_id(sensor_id: str) -> SensorModel:
  sensor = Sensor.objects(id=bson.ObjectId(sensor_id)).first()  # type: ignore
  if not sensor:
    raise HTTPException(status_code=404, detail='Sensor not found.')
  return sensor