from app.classes.visitor import Visitor
import time

class Simulation():
	def __init__(self, rooms, sensors):
			self.sensors = sensors
			self.rooms = rooms
			self.starting_room = rooms[0]
			self.visitors = []

	def run(self):
		while True:
			for visitor in self.visitors:
				visitor.move()
			for sensor in self.sensors:
				print(sensor.movements)
			self.visitors.append(Visitor(1, [self.starting_room]))
			time.sleep(5)