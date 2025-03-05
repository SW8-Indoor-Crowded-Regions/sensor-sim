import pytest
from unittest.mock import patch, MagicMock
from app.classes.sensor import Sensor 
from app.classes.room import Room
import os

@pytest.fixture
def sensor():
	room1 = Room({"id": 1, "name": "101", "type": "lounge"}, 1.5, 101.2, [])
	room2 = Room({"id": 2, "name": "102", "type": "exhibition"}, 1.2, 111.2, [])
	return Sensor(1, [room1, room2])

def test_pass_sensor(sensor):
	sensor.pass_sensor(1)
	assert sensor.movements == [0, 1]
	sensor.pass_sensor(2)
	assert sensor.movements == [1, 1]

def test_pass_sensor_invalid_room(sensor):
	with pytest.raises(Exception):
		sensor.pass_sensor(3)

@patch('app.classes.sensor.KafkaProducer')
@patch('app.classes.sensor.load_dotenv')
@patch('app.classes.sensor.os.getenv')
def test_send_data(mock_getenv, mock_load_dotenv, mock_kafka_producer, sensor):
	print(os.path.dirname(os.path.abspath(__file__)))
	mock_getenv.return_value = 'localhost:9092'
	mock_producer_instance = MagicMock()
	mock_kafka_producer.return_value = mock_producer_instance

	sensor.send_data()

	mock_load_dotenv.assert_called_once()
	mock_getenv.assert_called_once_with("KAFKA_BROKER")
	_, kwargs = mock_kafka_producer.call_args
	assert kwargs["bootstrap_servers"] == "localhost:9092"
	assert callable(kwargs["value_serializer"])
 
	mock_producer_instance.send.assert_called_once_with("sensor-data", value=sensor.movements)

@patch('app.classes.sensor.KafkaProducer')
@patch('app.classes.sensor.os.getenv', return_value='localhost:9092')
def test_send_data_message(mock_getenv, mock_kafka_producer, sensor):
    mock_producer_instance = MagicMock()
    mock_kafka_producer.return_value = mock_producer_instance
    
    sensor.movements = [3, 4]  # Set test data
    sensor.send_data()
    
    # Ensure correct topic and message
    mock_producer_instance.send.assert_called_once_with("sensor-data", value=[3, 4])
    
def test_pass_sensor_multiple_times(sensor):
    sensor.pass_sensor(1)
    sensor.pass_sensor(1)
    sensor.pass_sensor(2)
    assert sensor.movements == [1, 2]

def test_str(sensor):
	expected_str = "Sensor(id=1, rooms=[1, 2], movements=[0, 0])"
	assert str(sensor) == expected_str