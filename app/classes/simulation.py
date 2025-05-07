from app.classes.visitor import Visitor
from app.classes.room import Room
from app.classes.sensor import Sensor
from app.utils.heuristics import should_create_visitor, MovementConfig
import time


class Simulation:
	def __init__(
		self, rooms: list['Room'], sensors: list['Sensor'], config: MovementConfig, max_iterations=None, update_interval=1
	):
		self.rooms: list['Room'] = rooms
		self.sensors: list['Sensor'] = sensors
		self.starting_room: 'Room' = rooms[0]
		self.visitors: list['Visitor'] = []
		self.config = config
		self.max_iterations: None | int = max_iterations
		self.update_interval: int = update_interval

	def run(self) -> None:
		"""Runs the simulation."""
		entrance_sensor = Sensor(
			0,
			[
				Room({'id': 0, 'name': 'Entrance', 'type': 'ENTRANCE'}, 1.0, 1.0, 0, []),
				self.starting_room,
			],
		)
		iterations = 0
		try:
			while self.max_iterations is None or iterations < self.max_iterations:
				for visitor in self.visitors:
					visitor.move()
				for sensor in self.sensors:
					sensor.send_data()
				if should_create_visitor(self.config.create_visitor_probability):
					self.visitors.append(Visitor(1, [self.starting_room]))
					entrance_sensor.pass_sensor(0)
					entrance_sensor.send_data()
				time.sleep(5)
				iterations += 1
		except KeyboardInterrupt:  # pragma: no cover
			print('\nSimulation stopped.')
			exit()
