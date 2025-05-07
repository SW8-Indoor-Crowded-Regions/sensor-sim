from db import Database
from app.utils.load_objects import load_rooms, load_sensors
from app.classes.simulation import Simulation


def main():
	Database()
	# Run load_rooms function and store the result in the variable 'rooms'
	rooms = load_rooms()
	sensors = load_sensors(rooms)
	config = MovementConfig(
		alpha = 0.1
		beta = 0.1
		penalty_factor = 0.1
		create_visitor_probability = 0.5
	)

	simulation = Simulation(rooms, sensors, config)
	simulation.run()


if __name__ == '__main__':
	main()
