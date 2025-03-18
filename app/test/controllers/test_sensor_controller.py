import pytest
from fastapi import HTTPException
from unittest.mock import patch
import bson
from db.models.sensor import Sensor
from app.utils.data_models.sensors import SensorModel
from app.controllers.sensor_controller import (
	get_all_sensors,
	get_sensor_by_id,
	validate_sensor_id
)


# Sample sensor data
def sample_sensor() -> Sensor:
	return Sensor(
		id=bson.ObjectId(),
		name='Sensor A',
		rooms=[bson.ObjectId(), bson.ObjectId()],
	)


@pytest.fixture
def mock_sensors():
	return [
		SensorModel(
			id=bson.ObjectId(),
			rooms=[
				bson.ObjectId(),
				bson.ObjectId(),
			],

		),
		SensorModel(
			id=bson.ObjectId(),
			rooms=[
				bson.ObjectId(),
				bson.ObjectId(),
			],
		),
	]


@patch('db.models.sensor.Sensor.objects')
@patch('db.models.room.Room.objects')
@pytest.mark.asyncio
async def test_get_all_sensors(mock_objects, mock_sensors):
	mock_objects.return_value = mock_sensors
	sensors = await get_all_sensors()
	assert len(sensors) == len(mock_sensors)
	assert all(isinstance(sensor, Sensor) for sensor in sensors)


@patch('db.models.sensor.Sensor.objects')
@pytest.mark.asyncio
async def test_get_all_sensors_exception(mock_objects):
	mock_objects.side_effect = Exception('Database error')
	with pytest.raises(HTTPException) as exc:
		await get_all_sensors()
	assert exc.value.status_code == 500
	assert 'Database error' in exc.value.detail


@pytest.mark.parametrize(
	'sensor_id, is_valid',
	[
		(str(bson.ObjectId()), True),
		('invalid_id', False),
		('1234567890abcdef12345678', True),
		('12345', False),
	],
)
def test_validate_sensor_id(sensor_id, is_valid):
	if is_valid:
		validate_sensor_id(sensor_id)  # Should not raise an exception
	else:
		with pytest.raises(HTTPException) as exc:
			validate_sensor_id(sensor_id)
		assert exc.value.status_code == 400
		assert 'Invalid sensor id' in exc.value.detail


@patch('db.models.sensor.Sensor.objects')
@pytest.mark.asyncio
async def test_get_sensor_by_id_success(mock_objects):
	sensor = sample_sensor()
	mock_objects.return_value.no_dereference.return_value.first.return_value = sensor
	result = await get_sensor_by_id(str(sensor.id))  # type: ignore
	assert result == sensor


@patch('db.models.sensor.Sensor.objects')
@pytest.mark.asyncio
async def test_get_sensor_by_id_not_found(mock_objects):
	mock_objects.return_value.no_dereference.return_value.first.return_value = None
	with pytest.raises(HTTPException) as exc:
		await get_sensor_by_id(str(bson.ObjectId()))
	assert exc.value.status_code == 404
	assert 'Sensor not found' in exc.value.detail


@patch('db.models.sensor.Sensor.objects')
@pytest.mark.asyncio
async def test_get_sensor_by_id_internal_server_error(mock_fetch_sensor):
	mock_fetch_sensor.side_effect = Exception('Unexpected error')
	with pytest.raises(HTTPException) as exc:
		await get_sensor_by_id(str(bson.ObjectId()))
	assert exc.value.status_code == 500
	assert 'Unexpected error' in exc.value.detail
