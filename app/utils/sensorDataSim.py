import random
import time
import json
import os
# import room and sensor classes
from sensors.room import Room
from sensors.sensor import Sensor

current_dir = os.path.dirname(os.path.abspath(__file__))
sensors_file_path = os.path.join(current_dir, "sensors", "mockdata", "sensors.json")
rooms_file_path = os.path.join(current_dir, "sensors", "mockdata", "rooms.json")

def generate_sensor_data(sensor_id):
		"""Simulates sensor data with realistic crowd movement patterns."""
		return {
				"sensor_id": sensor_id,
				"timestamp": time.time(),
				"to_room1":  random.choices([0, 1, 2, 3, 4], weights=[0.8, 0.1, 0.05, 0.035, 0.015])[0],
		}
		
def intervalMovement(sensors, time):
		for sensor in sensors:
				room1 = sensor.getRoom1()
				room2 = sensor.getRoom2()

				# toRoom1: A number between 0 and the occupancy of room 2 (inclusive), with a higher probability of 0 and decreasing probability as the number increases
				toRoom1 = generate_sensor_data(room2, room1, time)
				toRoom2 = generate_sensor_data(room1, room2, time)
		
				# Change the occupancy of the rooms
				room1.changeOccupancy(toRoom1)
				room2.changeOccupancy(-toRoom1)
		
				room2.changeOccupancy(toRoom2)
				room1.changeOccupancy(-toRoom2)
		return sensors
				
	 
def generate_sensor_data(room1, room2, time):
	if room1.getName() == "ENTRANCE":
		if time > 20:
			return 0
		toRoom2 = random.choices(
				range(20),
				weights=[1] + [100 / (4 * (i + 1)) for i in range(1, 20)]
		)[0]
	else:
		if room1.getOccupancy() == 0:
				toRoom2 = 0
		else:
				max_occupancy = room1.getOccupancy()
				weights = [1] + [10 / (max_occupancy * (i + 1)) for i in range(1, max_occupancy + 1)]
				toRoom2 = random.choices(range(max_occupancy + 1), weights=weights)[0]
	return toRoom2
		
def initSensors():
		"""Simulates sensor data with realistic crowd movement patterns."""
		# Open json files for sensors and rooms and use them to create sensor and room objects using the classes
		with open(sensors_file_path) as f:
				sensor_data = json.load(f)
		
		rooms = {}
		sensors = []
		# Loop through the sensors and rooms to find the sensor data
		for sensor in sensor_data:
				room1Id = sensor.get('room1')
				room2Id = sensor.get('room2')
				
				if room1Id not in rooms:
						if room1Id == 'entrance':
								rooms[room1Id] = Room("ENTRANCE", "ENTRANCE")
						else:
								rooms[room1Id] = Room(room1Id, room1Id)
				
				if room2Id not in rooms:
						rooms[room2Id] = Room(room2Id, room2Id)
				
				room1 = rooms[room1Id]
				room2 = rooms[room2Id]
				
				sensors.append(Sensor(sensor.get('id'), room1, room2))
		
		return sensors, rooms
	 
if __name__ == "__main__":
		sensors, rooms = initSensors()
		for i in range(10):
				intervalMovement(sensors, 0)
				time.sleep(1)
		# while True:
		# 		for sensor_id in sensors:
		# 				sensor_data = generate_sensor_data(sensor_id)
		# 				producer.send(KAFKA_TOPIC, value=sensor_data)
		# 				print(f"Sent: {sensor_data}")
		# 		time.sleep(1)  # Simulate 1-second interval
	 