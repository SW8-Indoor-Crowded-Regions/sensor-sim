import pytest
from app.classes.room import Room
from app.classes.sensor import Sensor
from app.classes.visitor import Visitor

@pytest.fixture
def room_info():
	return {"id": 1, "name": "Conference Room", "type": "Meeting"}

@pytest.fixture
def sensors():
	return [Sensor(id=1, rooms=[]), Sensor(id=2, rooms=[])]

@pytest.fixture
def room(room_info, sensors):
	return Room(room_info, crowd_factor=1.5, area=50.0, sensors=sensors)

@pytest.fixture
def visitor():
  sensor1 = Sensor(1, [])
  sensor2 = Sensor(2, [])
  sensor3 = Sensor(3, [])
  room1 = Room({"id": 1, "name": "101", "type": "lounge"}, 1.5, 101.2, [sensor1, sensor2])
  room2 = Room({"id": 2, "name": "102", "type": "exhibition"}, 1.2, 111.2, [sensor1, sensor3])
  room3 = Room({"id": 3, "name": "103", "type": "meeting"}, 1.3, 121.2, [sensor2, sensor3])
  sensor1.rooms = [room1, room2]
  sensor2.rooms = [room1, room3]
  sensor3.rooms = [room2, room3]
  return Visitor(1, [room1, room2])

def test_get_movement_options(visitor):
  assert len(visitor.get_movement_options()) == 2
  assert visitor.get_movement_options()[0].id == 1
  assert visitor.get_movement_options()[1].id == 3

  assert visitor.get_movement_options()[0].rooms[0].id == 1
  assert visitor.get_movement_options()[0].rooms[1].id == 2

  assert visitor.get_movement_options()[1].rooms[0].id == 2
  assert visitor.get_movement_options()[1].rooms[1].id == 3
	
def test_move(visitor):
  assert visitor.get_current_room().id == 2
  visitor.move(visitor.get_movement_options()[0])
  print(visitor.visited_rooms)
  assert visitor.get_current_room().id == 1
  visitor.move(visitor.get_movement_options()[1])
  assert visitor.get_current_room().id == 3