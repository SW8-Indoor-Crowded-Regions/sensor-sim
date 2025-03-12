import pytest
from app.classes.room import Room
from app.classes.sensor import Sensor
from app.utils.load_objects import load_rooms, load_sensors

@pytest.fixture
def mock_rooms(mocker):
    """Mock database RoomModel.objects() call."""
    mock_room_data = [
        {"id": 1, "name": "Room 1", "type": "office", "crowd_factor": 1.5, "area": 50.0},
        {"id": 2, "name": "Room 2", "type": "conference", "crowd_factor": 2.0, "area": 100.0}
    ]
    
    mock_model = mocker.patch("app.utils.load_objects.RoomModel.objects", return_value=mock_room_data)
    return mock_model

@pytest.fixture
def mock_sensors(mocker):
    """Mock database SensorModel.objects() call."""
    mock_sensor_data = [
        mocker.Mock(id=1, rooms=[mocker.Mock(id=1), mocker.Mock(id=2)]),
        mocker.Mock(id=2, rooms=[mocker.Mock(id=2)])
    ]

    mock_model = mocker.patch("app.utils.load_objects.SensorModel.objects", return_value=mock_sensor_data)
    return mock_model

def test_load_rooms(mock_rooms):
    """Test that load_rooms correctly loads Room objects from the database."""
    
    rooms = load_rooms()
    
    assert len(rooms) == 2
    assert isinstance(rooms[0], Room)
    assert rooms[0].id == 1
    assert rooms[0].crowd_factor == 1.5
    assert rooms[0].area == 50.0

def test_load_sensors(mock_rooms, mock_sensors):
    """Test that load_sensors correctly loads Sensor objects and assigns rooms."""
    
    rooms = load_rooms()
    sensors = load_sensors(rooms)

    assert len(sensors) == 2
    assert isinstance(sensors[0], Sensor)
    assert sensors[0].id == 1
    assert len(sensors[0].rooms) == 2
    assert sensors[0].rooms[0].id == 1
    assert sensors[0].rooms[1].id == 2

    assert len(sensors[1].rooms) == 1
    assert sensors[1].rooms[0].id == 2

    # Check room-sensor relationships
    assert len(rooms[0].sensors) > 0
    assert sensors[0] in rooms[0].sensors
   
