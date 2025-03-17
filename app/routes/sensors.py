from fastapi import APIRouter
from app.controllers.sensor_controller import get_all_sensors, get_sensor_by_id
from app.utils.data_models.sensors import SensorListModel, SensorModel
from app.utils.response_examples.sensors import get_sensor_by_id_responses, get_sensors_responses

router = APIRouter(prefix='/sensors', tags=['Sensors'])

@router.get(
  '/',
  response_model=SensorListModel,
  summary='Get all sensors',
  tags=['Sensors'],
  response_description='Returns a list of all sensors.',
  description='Get all sensors from the database.',
  response_model_exclude_unset=True,
  responses=get_sensors_responses
)
async def fetch_sensors():
  """Get all sensors.
  Returns:
    dict: A dictionary containing a list of sensors.
  """
  sensors = get_all_sensors()
  return {'sensors': await sensors}


@router.get(
  '/{sensor_id}',
  response_model=SensorModel,
  summary='Get sensor by id',
  tags=['Sensors'],
  response_description='Returns a sensor by its id.',
  description='Get a sensor by its id.',
  response_model_exclude_unset=True,
  responses=get_sensor_by_id_responses,
)
async def fetch_sensor_by_id(sensor_id: str) -> SensorModel:
  """Get a sensor by its id.
  Args:
    sensor_id (str): The id of the sensor.
  Returns:
    dict: A dictionary containing the sensor.
  """
  sensor = get_sensor_by_id(sensor_id)
  return await sensor


