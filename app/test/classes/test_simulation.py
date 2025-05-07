import pytest
import time
from app.classes.visitor import Visitor
from app.classes.room import Room
from app.classes.simulation import Simulation
from app.utils.heuristics import MovementConfig


class StopSimulation(Exception):
	"""Custom exception to stop the infinite loop in the test."""

	pass


@pytest.fixture
def room():
	"""Fixture for creating a mock room."""
	return Room({'id': 0, 'name': 'Room 1', 'type': 'TEST'}, 1.0, 1.2, 100.0, [])


@pytest.fixture
def sensor():
	"""Fixture for creating a mock sensor."""

	class MockSensor:
		def send_data(self):
			pass  # Simulate sensor sending data without real logic

	return MockSensor()


@pytest.fixture
def config():
	"""MovementConfig fixture for mocking constants"""
	return MovementConfig(alpha=0.1, beta=0.1, penalty_factor=0.1, create_visitor_probability=0.5)


@pytest.fixture
def simulation(room, sensor, config):
	"""Fixture to initialize the simulation."""
	return Simulation(rooms=[room], sensors=[sensor], config=config)


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

	# Ensure that one visitor was added
	assert len(simulation.visitors) == 1
	assert isinstance(simulation.visitors[0], Visitor)


def test_visitor_movement(monkeypatch, simulation, config):
	"""Test that visitors move during simulation."""

	class MockVisitor:
		def __init__(self, id, rooms):
			self.id = id
			self.rooms = rooms
			self.moved = False

		def move(self):
			self.moved = True  # Simulate movement

	# Replace Visitor with MockVisitor
	monkeypatch.setattr('app.classes.visitor.Visitor', MockVisitor)

	# Add a visitor manually
	simulation.visitors.append(MockVisitor(1, [simulation.starting_room]))

	monkeypatch.setattr(time, 'sleep', lambda x: None)
	monkeypatch.setattr('app.classes.simulation.should_create_visitor', lambda cfg: False)

	# Add a counter to stop the infinite loop
	simulation.max_iterations = 2
	simulation.run()

	assert simulation.visitors[0].moved is True  # Ensure visitor moved
