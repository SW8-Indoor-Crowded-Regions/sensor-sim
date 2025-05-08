from db.models.room import Room
from db.models.sensor import Sensor
from db.database import Database
import json

db = Database()


def load_json(file_path):
	"""
	Load JSON data from a file.
	"""
	with open(file_path, 'r') as file:
		data = json.load(file)
	return data


def convert_oid_to_string(data):
	"""
	Recursively converts any '$oid' fields in the data to strings.
	"""
	if isinstance(data, dict):
		for key, value in data.items():
			if key == '$oid':
				data = value
			else:
				data[key] = convert_oid_to_string(value)
	elif isinstance(data, list):
		data = [convert_oid_to_string(item) for item in data]

	return data


def create_rooms_and_sensors():
	"""Creates Room documents for each labeled room in ROOM_ADJACENCY, and creates Sensor documents for each doorway/opening between rooms."""
	sensors = [Sensor(**data) for data in convert_oid_to_string(load_json('data/sensors_copy.json'))]
	room_data = convert_oid_to_string(load_json('data/rooms_copy.json'))

	rooms = []
	for data in room_data:
		room = Room(**data)
		room.area = room.compute_area()
		rooms.append(room)

	Sensor.objects.delete()  # type: ignore
	Room.objects.delete()  # type: ignore
	Sensor.objects.insert(sensors)  # type: ignore
	Room.objects.insert(rooms)  # type: ignore
	print('Rooms and sensors created successfully.')


create_rooms_and_sensors()
