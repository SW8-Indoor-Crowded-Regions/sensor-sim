from db import Database
from app.classes.consumer import Consumer
from app.utils.save_data import save_data

from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
	from app.classes.room import Room

class SensorRoomData(TypedDict):
    room_id: str
    movements: int

class SensorDataType(TypedDict):
    sensor_id: str
    room1: SensorRoomData
    room2: SensorRoomData

num_of_data = 0
rooms = []

def find_room_by_id(room_id: str, rooms: list['Room']) -> 'Room':
	"""Find a room by its ID."""
	room = next((room for room in rooms if str(room.id) == room_id), None)
	if not room:
		raise ValueError(f"Room {room_id} not found!")
	return room

def process_entrance_data(sensor_data: SensorDataType, rooms: list['Room']) -> list['Room']:
	"""Process data for entrance sensor."""
	room2 = find_room_by_id(sensor_data['room2']['room_id'], rooms)
	room2.add_occupants(sensor_data['room2']['movements'])
	
	people_leaving_room2 = sensor_data['room1']['movements']
	actual_removed_2 = min(people_leaving_room2, room2.occupancy)
	room2.remove_occupants(actual_removed_2)
	
	return rooms

def process_room_to_room_data(sensor_data: SensorDataType, rooms: list['Room']) -> list['Room']:
	"""Process data for room-to-room sensor."""
	room1 = find_room_by_id(sensor_data['room1']['room_id'], rooms)
	room2 = find_room_by_id(sensor_data['room2']['room_id'], rooms)
	
	# People moving from room1 to room2
	people_leaving_room1 = sensor_data['room2']['movements']
	actual_removed_1 = min(people_leaving_room1, room1.occupancy)
	room1.remove_occupants(actual_removed_1)
	room2.add_occupants(actual_removed_1)
	
	# People moving from room2 to room1
	people_leaving_room2 = sensor_data['room1']['movements']
	actual_removed_2 = min(people_leaving_room2, room2.occupancy)
	room2.remove_occupants(actual_removed_2)
	room1.add_occupants(actual_removed_2)
	
	return rooms

def update_room_occupancy(sensor_data: SensorDataType) -> tuple[str, list['Room']]:
	"""Updates the room occupancy based on the sensor data.
	Args:
		sensor_data (dict): The sensor data.
	"""
	global num_of_data, rooms
	if sensor_data['room1']['room_id'] == '0':
		rooms = process_entrance_data(sensor_data, rooms)
	else:
		rooms = process_room_to_room_data(sensor_data, rooms)
	
	if not sensor_data['sensor_id']:
		raise ValueError('Sensor ID is required.')
	
	if not rooms:
		raise ValueError('Rooms are required')

	num_of_data += 1
 
	if num_of_data % 100 == 0:
		save_data(rooms)

	return sensor_data['sensor_id'], rooms


def process_sensor_data(room_list: list['Room']) -> None:
	"""Processes the sensor data by consuming messages from the sensor-data topic and runs the calculate_crowd_factor function."""
	Database()
	global rooms
	rooms = room_list
	consumer = Consumer(update_room_occupancy, 'sensor-data')
	consumer.consume_messages()
