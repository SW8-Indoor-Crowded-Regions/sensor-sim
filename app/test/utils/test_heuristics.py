import pytest
from unittest.mock import MagicMock
from app.classes.visitor import Visitor
from app.classes.sensor import Sensor
from app.utils.heuristics import choose_next_move  # Adjust import path as needed

def test_choose_next_move():
    # Create a mock visitor
    visitor = MagicMock(spec=Visitor)
    
    # Create mock sensors to act as movement options
    sensor1 = MagicMock(spec=Sensor)
    sensor2 = MagicMock(spec=Sensor)
    sensor3 = MagicMock(spec=Sensor)
    
    # Define movement options
    movement_options = [sensor1, sensor2, sensor3]
    visitor.get_movement_options.return_value = movement_options
    
    # Run function multiple times to check randomness
    chosen_sensors = {choose_next_move(visitor) for _ in range(100)}
    
    # Ensure function only returns valid options
    assert chosen_sensors.issubset(set(movement_options))
    
    # Ensure all options are chosen at least once (high probability test)
    assert len(chosen_sensors) == len(movement_options)

def test_choose_next_move_no_options():
    # Create a mock visitor with no movement options
    visitor = MagicMock(spec=Visitor)
    visitor.get_movement_options.return_value = []
    
    # Expect an exception when no movement options are available
    with pytest.raises(Exception, match="No movement options found for visitor:"):
        choose_next_move(visitor)
