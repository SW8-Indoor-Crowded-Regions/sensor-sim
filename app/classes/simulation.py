from app.classes.visitor import Visitor
from app.utils.heuristics import should_create_visitor
import time
from app.classes.room import Room
from app.classes.sensor import Sensor

class Simulation():
	def __init__(self, rooms: list[Room], sensors: list[Sensor]):
			self.sensors = sensors
			self.rooms = rooms
			self.starting_room = rooms[0]
			self.visitors = []

	def run(self):
		entrance_sensor = Sensor(0, [Room({"id": 0, "name": "Entrance", "type": "ENTRANCE"}, 1.0, 0, []), self.starting_room])
		try:
			while True:
				for visitor in self.visitors:
					visitor.move()
				for sensor in self.sensors:
					sensor.send_data()
				if should_create_visitor():
					self.visitors.append(Visitor(1, [self.starting_room]))
					entrance_sensor.pass_sensor(0)
					entrance_sensor.send_data()
				time.sleep(5)
		except KeyboardInterrupt:
			print("\nSimulation stopped.")
			exit()