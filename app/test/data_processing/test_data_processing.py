import pytest
from app.classes.room import Room
from app.data_processing.data_processing import (
	update_room_occupancy,
	process_sensor_data,
	process_entrance_data,
	process_room_to_room_data,
)
from app.data_processing.data_processing import SensorDataType


@pytest.fixture
def rooms():
	"""Creates a set of Room objects for testing."""
	room1 = Room({'id': '1', 'name': 'Room 1', 'type': 'TEST'}, 0, 1.0, 1.0, 100.0, [])
	room2 = Room({'id': '2', 'name': 'Room 2', 'type': 'TEST'}, 0, 1.0, 1.0, 100.0, [])
	room3 = Room({'id': '3', 'name': 'Room 3', 'type': 'TEST'}, 0, 1.0, 1.0, 100.0, [])
	return [room1, room2, room3]


def test_process_entrance_data(rooms):
	"""Tests `process_entrance_data()` function."""
	sensor_data: SensorDataType = {
		'sensor_id': '1',
		'room1': {'room_id': '0', 'movements': 0},
		'room2': {'room_id': '1', 'movements': 3},
	}

	room1, room2, _ = rooms
	assert room2.occupancy == 0  # Initial state

	# Process entrance sensor data
	updated_rooms = process_entrance_data(sensor_data, rooms)

	# Room 2 should gain 3 occupants
	assert updated_rooms[0].occupancy == 3
	assert updated_rooms[1].occupancy == 0
	assert updated_rooms[2].occupancy == 0


def test_process_room_to_room_data(rooms):
	"""Tests `process_room_to_room_data()` function."""
	sensor_data: SensorDataType = {
		'sensor_id': '2',
		'room1': {'room_id': '1', 'movements': 2},
		'room2': {'room_id': '2', 'movements': 1},
	}

	room1, room2, _ = rooms
	room1.add_occupants(5)  # Start with 5 occupants
	room2.add_occupants(3)  # Start with 3 occupants

	assert room1.occupancy == 5
	assert room2.occupancy == 3

	# Process room-to-room sensor data
	updated_rooms = process_room_to_room_data(sensor_data, rooms)

	# Expected results:
	# Room 1 loses 1 occupant (min(1,5) = 1)
	# Room 2 gains 1 occupant
	# Room 2 loses 2 occupants (min(2,4) = 2)
	# Room 1 gains 2 occupants
	assert updated_rooms[0].occupancy == 6  # Room 1 now has 6
	assert updated_rooms[1].occupancy == 2  # Room 2 now has 2


def test_update_room_occupancy_entrance(rooms):
	"""Tests `update_room_occupancy()` when room1 is entrance (id=0)."""
	sensor_data: SensorDataType = {
		'sensor_id': '3',
		'room1': {'room_id': '0', 'movements': 0},
		'room2': {'room_id': '1', 'movements': 2},
	}

	room1, room2, _ = rooms
	assert room1.occupancy == 0
	assert room2.occupancy == 0

	sensor_id, updated_rooms = update_room_occupancy(sensor_data, rooms)

	assert sensor_id == '3'
	assert updated_rooms[0].occupancy == 2


def test_update_room_occupancy_room_to_room(rooms):
	"""Tests `update_room_occupancy()` when moving between two rooms."""
	sensor_data: SensorDataType = {
		'sensor_id': '4',
		'room1': {'room_id': '1', 'movements': 1},
		'room2': {'room_id': '2', 'movements': 3},
	}

	rooms[0].add_occupants(5)  # Room 1 starts with 5 occupants
	rooms[1].add_occupants(2)  # Room 2 starts with 2 occupants

	sensor_id, updated_rooms = update_room_occupancy(sensor_data, rooms)

	assert sensor_id == '4'
	assert updated_rooms[0].occupancy == 3  # Room 1 gains 1-3=-2 occupant
	assert updated_rooms[1].occupancy == 4  # Room 2 gains 3-1=2 occupants


def test_update_room_occupancy_invalid_sensor_id(rooms):
	"""Tests `update_room_occupancy()` with a missing sensor ID."""
	sensor_data: SensorDataType = {
		'sensor_id': '',
		'room1': {'room_id': '1', 'movements': 2},
		'room2': {'room_id': '2', 'movements': 1},
	}

	with pytest.raises(ValueError, match='Sensor ID is required.'):
		update_room_occupancy(sensor_data, rooms)


def test_update_room_occupancy_invalid_room_id(rooms):
	"""Tests `update_room_occupancy()` with a non-existent room ID."""
	sensor_data: SensorDataType = {
		'sensor_id': '5',
		'room1': {'room_id': '99', 'movements': 1},  # Invalid room ID
		'room2': {'room_id': '2', 'movements': 1},
	}

	with pytest.raises(ValueError, match='Room 99 not found!'):
		update_room_occupancy(sensor_data, rooms)


def test_update_room_occupancy_invalid_rooms(rooms, monkeypatch):
	"""Tests `update_room_occupancy()` with missing rooms."""
	sensor_data: SensorDataType = {
		'sensor_id': '6',
		'room1': {'room_id': '1', 'movements': 1},
		'room2': {'room_id': '2', 'movements': 1},
	}

	monkeypatch.setattr(
		'app.data_processing.data_processing.process_room_to_room_data', lambda x, y: None
	)

	with pytest.raises(ValueError, match='Rooms are required'):
		update_room_occupancy(sensor_data, rooms)


def test_update_room_occupancy_save_data(rooms, monkeypatch, mocker):
	"""Tests `update_room_occupancy()` with saving data every 100 updates."""
	sensor_data: SensorDataType = {
		'sensor_id': '7',
		'room1': {'room_id': '1', 'movements': 2},
		'room2': {'room_id': '2', 'movements': 1},
	}

	save_data_mock = mocker.patch('app.data_processing.data_processing.save_data')
	monkeypatch.setattr('app.data_processing.data_processing.num_of_data', 98)
	rooms[0].add_occupants(1)
	rooms[1].add_occupants(2)

	sensor_id, updated_rooms = update_room_occupancy(sensor_data, rooms)

	assert sensor_id == '7'
	assert updated_rooms[0].occupancy == 2
	assert updated_rooms[1].occupancy == 1
	save_data_mock.assert_not_called()

	sensor_id, updated_rooms = update_room_occupancy(sensor_data, updated_rooms)
	assert sensor_id == '7'
	assert updated_rooms[0].occupancy == 3
	assert updated_rooms[1].occupancy == 0
	save_data_mock.assert_called_once_with(updated_rooms)


def test_process_sensor_data(monkeypatch, mocker, rooms):
	"""Tests `process_sensor_data()` function."""
	monkeypatch.setattr('app.data_processing.data_processing.Database', lambda: None)

	mock_consumer = mocker.patch('app.data_processing.data_processing.Consumer')
	process_sensor_data(rooms)

	mock_consumer.assert_called_once_with(update_room_occupancy, 'sensor-data', rooms)


def test_100_runs(rooms, monkeypatch):
	from app.data_processing.data_processing import update_room_occupancy, SensorDataType
	import random

	updated_rooms = rooms

	monkeypatch.setattr('app.data_processing.data_processing.save_data', lambda x: None)

	for i in range(100):
		sensor_data: SensorDataType = {
			'sensor_id': f'loop_{i}',
			'room1': {
				'room_id': str(random.choice(['0', '1', '2'])),
				'movements': random.randint(0, 5),
			},
			'room2': {
				'room_id': str(random.choice(['1', '2'])),
				'movements': random.randint(0, 5),
			},
		}
		_, updated_rooms = update_room_occupancy(sensor_data, rooms)

	for room in updated_rooms:
		assert room.occupancy >= 0, 'Occupancy should never go negative'
	assert any(room.occupancy > 0 for room in updated_rooms), (
		'At least one room should have occupants'
	)
