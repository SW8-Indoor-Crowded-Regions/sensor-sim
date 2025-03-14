import sys
import os
from db import Database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.load_objects import load_rooms, load_sensors
from app.classes.simulation import Simulation


def main():
	Database()
	# Run load_rooms function and store the result in the variable 'rooms'
	rooms = load_rooms()
	sensors = load_sensors(rooms)

	simulation = Simulation(rooms, sensors)
	simulation.run()


if __name__ == '__main__':
	main()
