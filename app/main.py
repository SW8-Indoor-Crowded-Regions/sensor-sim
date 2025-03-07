import sys
import os
from db import Database
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.loadObjects import load_rooms, load_sensors
from app.classes.simulation import Simulation

def main():
	Database()
	# Run load_rooms function and store the result in the variable 'rooms'
	rooms = load_rooms()
	sensors = load_sensors(rooms)

	# Print the rooms and sensors with __str__ method
	print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
	print("Rooms:")
	for room in rooms:
		print("	", room)
	print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
	print("Sensors:")
	for sensor in sensors:
		print("	", sensor)
	print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————")

	simulation = Simulation(rooms, sensors)
	simulation.run()

	


if __name__ == "__main__":
	main()