from app.classes.visitor import Visitor
from app.utils.heuristics import should_create_visitor
import time

class Simulation():
	def __init__(self, rooms, sensors, max_iterations=None):
			self.sensors = sensors
			self.rooms = rooms
			self.starting_room = rooms[0]
			self.visitors = []
			self.max_iterations = max_iterations

	def run(self):
		iterations = 0
		try:
			while self.max_iterations is None or iterations < self.max_iterations:
				for visitor in self.visitors:
					visitor.move()
				for sensor in self.sensors:
					sensor.send_data()
				if should_create_visitor():
					self.visitors.append(Visitor(1, [self.starting_room])) 
				time.sleep(5)
				iterations += 1
		except KeyboardInterrupt: # pragma: no cover
			print("\nSimulation stopped.") 
			exit()