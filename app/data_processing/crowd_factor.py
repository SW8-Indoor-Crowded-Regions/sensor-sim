import os
import sys
from db import Database

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.classes.consumer import Consumer
from app.utils.loadObjects import load_rooms, load_sensors



Database()
rooms = load_rooms()
sensors = load_sensors(rooms)

def calculate_crowd_factor(sensor_data: dict[str, dict[str, int]]):
	"""Calculates the crowdedness of the rooms based on the sensor data.
	Args:
		sensor_data (dict): The sensor data.	 
  """
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
 
	

def process_sensor_data():
	""" Processes the sensor data by consuming messages from the sensor-data topic and runs the calculate_crowd_factor function.
	"""
	consumer = Consumer(calculate_crowd_factor, "sensor-data")
	consumer.consume_messages()


if __name__ == "__main__":
	process_sensor_data()