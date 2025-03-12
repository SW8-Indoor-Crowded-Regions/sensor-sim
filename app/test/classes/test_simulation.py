import pytest
import time
from app.classes.visitor import Visitor
from app.classes.room import Room
from app.classes.simulation import Simulation

class StopSimulation(Exception):
		"""Custom exception to stop the infinite loop in the test."""
		pass

@pytest.fixture
def room():
		"""Fixture for creating a mock room."""
		return Room({"id": 0, "name": "Room 1", "type": "TEST"}, 1.0, 100.0, [])

@pytest.fixture
def sensor():
		"""Fixture for creating a mock sensor."""
		class MockSensor:
				def send_data(self):
						pass  # Simulate sensor sending data without real logic

		return MockSensor()

@pytest.fixture
def simulation(room, sensor):
		"""Fixture to initialize the simulation."""
		return Simulation(rooms=[room], sensors=[sensor])

def test_simulation_runs(monkeypatch, simulation):
		"""Test that the simulation runs and adds a visitor correctly."""
		
		# Patch time.sleep to avoid real delays
		monkeypatch.setattr(time, "sleep", lambda x: None)

		# Patch should_create_visitor to return True once, then False
		visitor_creation = iter([True, False, False])  
		monkeypatch.setattr("app.classes.simulation.should_create_visitor", lambda: next(visitor_creation))
		monkeypatch.setattr("app.classes.visitor.Visitor.move", lambda x: None)
		monkeypatch.setattr("app.classes.sensor.Sensor.send_data", lambda x: None)

		# Add a counter to stop the infinite loop
		max_iterations = 2

		simulation.max_iterations = max_iterations

		# Run the simulation and expect it to stop after 2 iterations
		simulation.run()
		
		# Ensure that one visitor was added
		assert len(simulation.visitors) == 1
		assert isinstance(simulation.visitors[0], Visitor)

def test_visitor_movement(monkeypatch, simulation):
		"""Test that visitors move during simulation."""

		class MockVisitor:
				def __init__(self, id, rooms):
						self.id = id
						self.rooms = rooms
						self.moved = False

				def move(self):
						self.moved = True  # Simulate movement

		# Replace Visitor with MockVisitor
		monkeypatch.setattr("app.classes.visitor.Visitor", MockVisitor)

		# Add a visitor manually
		simulation.visitors.append(MockVisitor(1, [simulation.starting_room]))

		monkeypatch.setattr(time, "sleep", lambda x: None)
		monkeypatch.setattr("app.classes.simulation.should_create_visitor", lambda: False)

		# Add a counter to stop the infinite loop
		max_iterations = 2
		simulation.max_iterations = max_iterations

		simulation.run()
	
		assert simulation.visitors[0].moved is True  # Ensure visitor moved