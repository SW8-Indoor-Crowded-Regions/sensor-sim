from db import Database
from app.classes.consumer import Consumer
from app.utils.load_objects import load_rooms


def update_room_occupancy(sensor_data: dict[str, dict[str, int]]):
	"""Updates the room occupancy based on the sensor data.
	Args:
		sensor_data (dict): The sensor data.	 
	"""
	rooms = load_rooms()
	if sensor_data["room1"]["room_id"] == "0":
		room2 = [room for room in rooms if room.id.__str__() == sensor_data["room2"]["room_id"]][0]
		room2.add_occupants(sensor_data["room2"]["movements"])
		room2.remove_occupants(sensor_data["room1"]["movements"])
		return
	
	room1 = [room for room in rooms if room.id.__str__() == sensor_data["room1"]["room_id"]][0]
	room2 = [room for room in rooms if room.id.__str__() == sensor_data["room2"]["room_id"]][0]
	
	room1.add_occupants(sensor_data["room1"]["movements"])
	room1.remove_occupants(sensor_data["room2"]["movements"])
	room2.add_occupants(sensor_data["room2"]["movements"])
	room2.remove_occupants(sensor_data["room1"]["movements"])
 
	

def process_sensor_data() -> None:
	""" Processes the sensor data by consuming messages from the sensor-data topic and runs the calculate_crowd_factor function.
	"""
	Database()
	consumer = Consumer(update_room_occupancy, "sensor-data")
	consumer.consume_messages()