import pytest
from app.classes.sensor import Sensor
from app.classes.room import Room


@pytest.fixture
def sensor():
	room1 = Room({'id': 1, 'name': '101', 'type': 'lounge'}, 1.5, 1.2, 101.2, [])
	room2 = Room({'id': 2, 'name': '102', 'type': 'exhibition'}, 1.2, 1.2, 111.2, [])
	return Sensor(1, [room1, room2])


def test_pass_sensor(sensor):
	sensor.pass_sensor(1)
	assert sensor.movements == [0, 1]
	sensor.pass_sensor(2)
	assert sensor.movements == [1, 1]


def test_pass_sensor_invalid_room(sensor):
	with pytest.raises(Exception):
		sensor.pass_sensor(3)


def test_pass_sensor_multiple_times(sensor):
	sensor.pass_sensor(1)
	sensor.pass_sensor(1)
	sensor.pass_sensor(2)
	assert sensor.movements == [1, 2]


def test_send_data(mocker, sensor):
	mocker.patch('app.classes.sensor.send_data')
	sensor.send_data()
	assert sensor.movements == [0, 0]
	sensor.movements = [1, 2]
	sensor.send_data()
	assert sensor.movements == [0, 0]


def test_str(sensor):
	expected_str = "Sensor(id=1, rooms=['Room id: 1', 'Room id: 2'], movements=[0, 0])"
	assert str(sensor) == expected_str
