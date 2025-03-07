from app.classes.visitor import Visitor
from app.utils.kafka_producer import send_data
from app.utils.heuristics import should_create_visitor
import time

class Simulation():
	def __init__(self, rooms, sensors):
			self.sensors = sensors
			self.rooms = rooms
			self.starting_room = rooms[0]
			self.visitors = []

	def run(self):
		try:
			while True:
				for visitor in self.visitors:
					visitor.move()
				for sensor in self.sensors:
					sensor.send_data()
				if should_create_visitor():
					self.visitors.append(Visitor(1, [self.starting_room])) 
				time.sleep(5)
		except KeyboardInterrupt:
			print("\nSimulation stopped.")
			exit()