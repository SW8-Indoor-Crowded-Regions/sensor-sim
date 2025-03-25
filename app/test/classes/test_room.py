import pytest
from app.classes.room import Room
from app.classes.sensor import Sensor


@pytest.fixture
def room_info():
	return {'id': 1, 'name': 'Conference Room', 'type': 'Meeting'}


@pytest.fixture
def sensors():
	return [Sensor(id=1, rooms=[]), Sensor(id=2, rooms=[])]


@pytest.fixture
def room(room_info, sensors):
	return Room(room_info, crowd_factor=1.5, area=50.0, sensors=sensors)


def test_room_initialization(room, room_info, sensors):
	assert room.id == room_info['id']
	assert room.name == room_info['name']
	assert room.type == room_info['type']
	assert room.occupancy == 0
	assert room.crowd_factor == 1.5
	assert room.area == 50.0
	assert room.sensors == sensors


def test_add_occupants(room):
	room.add_occupants(1)
	assert room.occupancy == 1


def test_remove_occupants(room):
	room.add_occupants(3)
	room.remove_occupants(2)
	assert room.occupancy == 1


def test_remove_occupants_below_zero(room):
	room.remove_occupants(1)
	assert room.occupancy == 0


def test_str(room):
	expected_str = "Room (id=1, name=Conference Room, type=Meeting, occupancy=0, crowdFactor=1.5, area=50.0, sensors=['Sensor id: 1', 'Sensor id: 2'])"
	assert str(room) == expected_str
