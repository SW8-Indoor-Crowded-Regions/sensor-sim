from app.classes.room import Room
from app.classes.sensor import Sensor
from db import Room as RoomModel, Sensor as SensorModel


def load_rooms() -> list[Room]:
	"""Load rooms from the rooms.json file and return a list of Room objects.
	Returns:
		list[Room]: A list of Room objects.
	"""
	rooms = []
	room_data = RoomModel.objects()  # type: ignore
	for room in room_data:
		rooms.append(Room(room, room['crowd_factor'], room['popularity_factor'], room['area'], []))
	return rooms


def load_sensors(rooms: list['Room']) -> list[Sensor]:
	"""Load sensors from the database and return a list of Sensor objects.
	Returns:
			list[Sensor]: A list of Sensor objects.
	"""
	sensors = []
	sensor_data = SensorModel.objects()  # type: ignore
	for sensor in sensor_data:
		sensor_rooms = []
		for sensor_room in sensor.rooms:
			sensor_rooms.append(list(filter(lambda room: room.id == sensor_room.id, rooms))[0])
		new_sensor = Sensor(sensor.id, sensor_rooms)
		new_sensor.rooms = sensor_rooms
		for room in sensor_rooms:
			room.sensors.append(new_sensor)
		sensors.append(new_sensor)
	return sensors
