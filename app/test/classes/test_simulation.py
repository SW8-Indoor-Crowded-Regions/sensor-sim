import pytest
import time
from datetime import timedelta
from app.classes.visitor import Visitor
from app.classes.room import Room
from app.classes.sensor import Sensor
from app.classes.simulation import Simulation
from app.utils.heuristics import MovementConfig


class StopSimulation(Exception):
	"""Custom exception to stop the infinite loop in the test."""

	pass


@pytest.fixture
def room():
	"""Fixture for creating a mock room."""
	return Room({'id': 0, 'name': 'Room 1', 'type': 'TEST'}, occupancy=0, crowd_factor=1.0, popularity_factor=1.2, area=100.0, sensors=[])


@pytest.fixture
def sensor():
	"""Fixture for creating a mock sensor."""

	class MockSensor:
		def __init__(self, id, rooms):
			self.id = id
			self.rooms = rooms
			self.movements = [0,0]

		def send_data(self):
			pass  # Simulate sensor sending data without real logic

	return MockSensor(1, [room, room_with_occupancy])


@pytest.fixture
def config():
	"""MovementConfig fixture for mocking constants"""
	return MovementConfig(alpha=0.1, beta=0.1, penalty_factor=0.1, create_visitor_probability=0.5)


@pytest.fixture
def simulation(room, sensor, config):
	"""Fixture to initialize the simulation."""
	return Simulation(rooms=[room], sensors=[sensor], config=config)


@pytest.fixture
def room_with_occupancy():
	"""Fixture for creating a room with specified occupancy."""
	room = Room({'id': 1, 'name': 'Gallery', 'type': 'Exhibition'}, 0, 1.0, 1.0, 100.0, [])
	room.occupancy = 3  # Set occupancy to 3
	return room

@pytest.fixture
def simulation_with_occupancy(room_with_occupancy, sensor, config):
	"""Fixture to initialize the simulation with room occupancy."""
	return Simulation(rooms=[room_with_occupancy], sensors=[sensor], config=config)


def test_simulation_runs(monkeypatch, simulation, config):
	"""Test that the simulation runs and adds a visitor correctly."""

	# Patch time.sleep to avoid real delays
	monkeypatch.setattr(time, 'sleep', lambda _: None)

	# Patch should_create_visitor to return True once, then False
	visitor_creation = iter([True, False, False])
	monkeypatch.setattr(
		'app.classes.simulation.should_create_visitor', lambda cfg: next(visitor_creation)
	)
	monkeypatch.setattr('app.classes.visitor.Visitor.move', lambda self: None)
	monkeypatch.setattr('app.classes.sensor.Sensor.send_data', lambda self: None)

	# Add a counter to stop the infinite loop
	simulation.max_iterations = 2

	# Run the simulation and expect it to stop after 2 iterations
	simulation.run()

	# Ensure that 1 visitor was added by simulation
	assert len(simulation.visitors) == 1
	assert isinstance(simulation.visitors[0], Visitor)


def test_visitor_movement(monkeypatch, simulation, config):
	"""Test that visitors move during simulation."""

	class MockVisitor:
		def __init__(self, id, rooms, config):
			self.id = id
			self.rooms = rooms
			self.moved = False
			self.config = config

		def move(self):
			self.moved = True  # Simulate movement

	# Replace Visitor with MockVisitor
	monkeypatch.setattr('app.classes.visitor.Visitor', MockVisitor)

	# Add a visitor manually
	simulation.visitors.append(MockVisitor(1, [simulation.starting_room], config))

	monkeypatch.setattr(time, 'sleep', lambda x: None)
	monkeypatch.setattr('app.classes.simulation.should_create_visitor', lambda cfg: False)

	# Add a counter to stop the infinite loop
	simulation.max_iterations = 2
	simulation.run()

	assert simulation.visitors[0].moved is True  # Ensure visitor moved


def test_update_interval_timedelta():
	seconds = timedelta(seconds=3600)
	minutes = timedelta(minutes=60)
	hours = timedelta(hours=1)

	assert seconds.total_seconds() == 3600
	assert minutes.total_seconds() == 3600
	assert hours.total_seconds() == 3600


def test_create_visitors_from_occupancy(simulation_with_occupancy):
	"""Test that visitors are created based on room occupancy at initialization."""
	simulation = simulation_with_occupancy
	visitors = simulation.visitors

	assert len(visitors) == 3, f"Expected 3 visitors but found {len(visitors)}"
	# Check if each visitor is correctly associated with the starting room and the current roo
	for visitor in visitors:
		assert isinstance(visitor, Visitor)
		# Ensure that 2 visitors were added based on room occupancy
		assert len(visitor.visited_rooms) == 2
		assert visitor.visited_rooms[0].id == simulation.starting_room.id 
		assert visitor.visited_rooms[1].id == 1 


def test_create_visitors_with_previous_room():
	"""Test that visitors are created with a previous room if a sensor connects to it."""
	starting_room = Room({'id': 0, 'name': 'Entrance', 'type': 'ENTRANCE'}, 0, 1.0, 1.0, 0, [])
	previous_room = Room({'id': 1, 'name': 'Gallery', 'type': 'Exhibition'}, 0, 1.0, 1.0, 100.0, [])
	current_room = Room({'id': 2, 'name': 'Room 2', 'type': 'TEST'}, 0, 1.0, 1.2, 100.0, [])
	current_room.occupancy = 2

	# Define a sensor that connects previous_room and current_room
	sensor = Sensor(1, [previous_room, current_room])

	config = MovementConfig(alpha=0.1, beta=0.1, penalty_factor=0.1, create_visitor_probability=0.5)

	simulation = Simulation(rooms=[starting_room, previous_room, current_room], sensors=[sensor], config=config)

	assert len(simulation.visitors) == 2, f"Expected 2 visitors, got {len(simulation.visitors)}"

	for visitor in simulation.visitors:
		assert len(visitor.visited_rooms) == 3, f"Expected 3 visited rooms, got {len(visitor.visited_rooms)}"
		assert visitor.visited_rooms[0].id == starting_room.id
		assert visitor.visited_rooms[1].id == previous_room.id
		assert visitor.visited_rooms[2].id == current_room.id
