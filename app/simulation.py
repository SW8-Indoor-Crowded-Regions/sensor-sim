from db import Database
from app.utils.load_objects import load_rooms, load_sensors
from app.classes.simulation import Simulation
from app.utils.heuristics import MovementConfig
from datetime import timedelta


def main():
	Database()
	# Run load_rooms function and store the result in the variable 'rooms'
	rooms = load_rooms()
	sensors = load_sensors(rooms)

	# Movement Heuristics:
	#   - alpha = significance/weight assigned to the popularity factor of a room
	#   - beta = significance/weight assigned to area of a room
	#   - penalty_factor = weight that acts as penalty to avoid backtracking to previous room
	#   - create_visitor_probability = likelihood of new visitor being created
	config = MovementConfig(alpha=0.1, beta=0.1, penalty_factor=0.1, create_visitor_probability=0.5)

	# To change the update_interval of the simulation, have a look at below examples:
	#   - timedelta(seconds=x)
	#   - timedelta(minutes=x)
	#   - timedelta(hours=x)
	# Replace x with the amount you prefer
	simulation = Simulation(rooms=rooms, sensors=sensors, config=config, max_iterations=None, update_interval=timedelta(seconds=10))
	simulation.run()


if __name__ == '__main__':
	main()
