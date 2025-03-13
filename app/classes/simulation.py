from app.classes.visitor import Visitor
from app.utils.heuristics import should_create_visitor
import time
from app.classes.room import Room
from app.classes.sensor import Sensor

class Simulation():
	def __init__(self, rooms: list[Room], sensors: list[Sensor], max_iterations=None):
			self.sensors = sensors
			self.rooms = rooms
			self.starting_room = rooms[0]
			self.visitors = []
			self.max_iterations = max_iterations

	def run(self) -> None:
		"""Runs the simulation."""
		entrance_sensor = Sensor(0, [Room({"id": 0, "name": "Entrance", "type": "ENTRANCE"}, 1.0, 0, []), self.starting_room])
		iterations = 0
		try:
			while self.max_iterations is None or iterations < self.max_iterations:
				for visitor in self.visitors:
					visitor.move()
				for sensor in self.sensors:
					sensor.send_data()
				if should_create_visitor():
					self.visitors.append(Visitor(1, [self.starting_room]))
					entrance_sensor.pass_sensor(0)
					entrance_sensor.send_data()
				time.sleep(5)
				iterations += 1
		except KeyboardInterrupt: # pragma: no cover
			print("\nSimulation stopped.") 
			exit()