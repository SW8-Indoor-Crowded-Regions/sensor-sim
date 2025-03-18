import pytest
from app.classes.room import Room
from app.data_processing.data_processing import update_room_occupancy, process_sensor_data


@pytest.fixture
def rooms():
	"""Creates a set of Room objects for testing."""
	room1 = Room({'id': 1, 'name': 'Room 1', 'type': 'TEST'}, 1.0, 100.0, [])
	room2 = Room({'id': 2, 'name': 'Room 2', 'type': 'TEST'}, 1.0, 100.0, [])
	room3 = Room({'id': 3, 'name': 'Room 3', 'type': 'TEST'}, 1.0, 100.0, [])
	return [room1, room2, room3]


@pytest.fixture
def sensors(rooms):
	"""Creates mock sensors associated with rooms."""
	return [
		{'id': '1', 'rooms': [rooms[0], rooms[1]]},
		{'id': '2', 'rooms': [rooms[0], rooms[2]]},
		{'id': '3', 'rooms': [rooms[1], rooms[2]]},
	]


@pytest.fixture
def sensor_data():
	"""Provides test sensor data with movements between rooms."""
	return [
		{'sensor_id': '0', 'room1': {'room_id': '0', 'movements': 0}, 'room2': {'room_id': '1', 'movements': 2}},
		{'sensor_id': '1', 'room1': {'room_id': '1', 'movements': 0}, 'room2': {'room_id': '2', 'movements': 1}},
		{'sensor_id': '2', 'room1': {'room_id': '2', 'movements': 1}, 'room2': {'room_id': '3', 'movements': 1}},
	]


def test_calculate_crowd_factor(rooms, sensor_data, monkeypatch):
	"""Tests if `calculate_crowd_factor()` updates room occupancy correctly."""

	# Patch the global `rooms` list used inside `calculate_crowd_factor`
	monkeypatch.setattr('app.data_processing.data_processing.Database', lambda: None)

	# Initial occupant count
	room1, room2, room3 = rooms
	assert room1.occupancy == 0
	assert room2.occupancy == 0

	expected_occupancy = [[2, 0, 0], [1, 1, 0], [1, 1, 0]]

	for idx, data in enumerate(sensor_data):
		update_room_occupancy(data, rooms)
		assert room1.occupancy == expected_occupancy[idx][0]
		assert room2.occupancy == expected_occupancy[idx][1]
		assert room3.occupancy == expected_occupancy[idx][2]


def test_calculate_crowd_factor_with_room1_zero(rooms, monkeypatch):
	"""Tests `calculate_crowd_factor()` when `room1["room_id"] == "0"` case."""

	# Patch the global `rooms` list
	monkeypatch.setattr('app.data_processing.data_processing.Database', lambda: None)

	# Import SensorDataType for proper typing
	from app.data_processing.data_processing import SensorDataType

	# Sensor data where room1 is "0"
	sensor_data: SensorDataType = {
		'sensor_id': '1',
		'room1': {'room_id': '0', 'movements': 2},
		'room2': {'room_id': '1', 'movements': 4},
	}

	room1, room2, room3 = rooms
	assert room1.occupancy == 0
	assert room2.occupancy == 0

	update_room_occupancy(sensor_data, rooms)

	# Ensure that room1 occupancy is updated correctly
	assert room1.occupancy == 2
	assert room2.occupancy == 0
	assert room3.occupancy == 0


def test_process_sensor_data(monkeypatch, mocker, rooms):
	"""Tests `process_sensor_data()` function."""

	monkeypatch.setattr('app.data_processing.data_processing.Database', lambda: None)

	mock_consumer = mocker.patch('app.data_processing.data_processing.Consumer')
	process_sensor_data(rooms)
	mock_consumer.assert_called_once_with(update_room_occupancy, 'sensor-data', rooms)
