from app.classes.visitor import Visitor
from app.classes.room import Room
from app.classes.sensor import Sensor
from app.utils.heuristics import should_create_visitor, MovementConfig
from datetime import timedelta
import time


class Simulation:
	def __init__(
		self,
		rooms: list['Room'],
		sensors: list['Sensor'],
		config: MovementConfig,
		max_iterations=None,
		update_interval: timedelta = timedelta(seconds=5),
	):
		self.rooms: list['Room'] = rooms
		self.sensors: list['Sensor'] = sensors
		self.starting_room: 'Room' = rooms[0]
		self.config: MovementConfig = config
		self.max_iterations: None | int = max_iterations
		self.update_interval: timedelta = update_interval
		self.visitors: list['Visitor'] = self.init_visitors_from_rooms()

	def init_visitors_from_rooms(self) -> list['Visitor']:
		"""Initialize visitors from rooms with exisiting occupants"""
		visitors = []
		for room in self.rooms:
			for _ in range(room.occupancy):
				previous_room = None
				for sensor in self.sensors:
					if room in sensor.rooms:
						previous_room = next(r for r in sensor.rooms if r != room)
						break

				if previous_room:
					visitors.append(Visitor(1, [self.starting_room, previous_room, room], self.config))
				else:
					visitors.append(Visitor(1, [self.starting_room, room], self.config))
		return visitors

	def run(self) -> None:
		"""Runs the simulation."""
		entrance_sensor = Sensor(
			0,
			[
				Room({'id': 0, 'name': 'Entrance', 'type': 'ENTRANCE'}, 0, 1.0, 1.0, 0, []),
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
				if should_create_visitor(self.config):
					self.visitors.append(Visitor(1, [self.starting_room], self.config))
					entrance_sensor.pass_sensor(0)
					entrance_sensor.send_data()

				time.sleep(self.update_interval.total_seconds())
				iterations += 1
		except KeyboardInterrupt:  # pragma: no cover
			print('\nSimulation stopped.')
			exit()
