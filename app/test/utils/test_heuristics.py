import pytest
from app.classes.visitor import Visitor
from app.classes.sensor import Sensor
from app.classes.room import Room
from app.utils.heuristics import choose_next_move, should_create_visitor, get_weights


@pytest.fixture
def rooms():
	return [
		Room({'id': 1, 'name': '101', 'type': 'lounge'}, 1.5, 1.2, 101.2, []),
		Room({'id': 2, 'name': '102', 'type': 'exhibition'}, 1.2, 1.2, 111.2, []),
		Room({'id': 3, 'name': '103', 'type': 'meeting'}, 1.3, 1.2, 121.2, []),
	]


@pytest.fixture
def sensors(rooms):
	return [
		Sensor(1, [rooms[0], rooms[1]]),
		Sensor(2, [rooms[0], rooms[2]]),
		Sensor(3, [rooms[1], rooms[2]]),
	]


@pytest.fixture
def visitor(rooms):
	return Visitor(1, [rooms[0], rooms[1]])


@pytest.fixture
def setup_rooms_and_visitor(sensors, rooms, visitor):
	rooms[0].sensors = [sensors[0], sensors[1]]
	rooms[1].sensors = [sensors[0], sensors[2]]
	rooms[2].sensors = [sensors[1], sensors[2]]

	visitor.get_movement_options = lambda: [sensors[0], sensors[1], sensors[2]]
	visitor.get_current_room = lambda: rooms[1]
	return visitor


def test_choose_next_move(setup_rooms_and_visitor):
	visitor = setup_rooms_and_visitor

	# Run function multiple times to check randomness
	chosen_sensors = {choose_next_move(visitor) for _ in range(100)}

	# Ensure function only returns valid options
	assert chosen_sensors.issubset(set(visitor.get_movement_options()).union({None}))

	# Ensure all options are chosen at least once (high probability test)
	assert len(chosen_sensors) == len(visitor.get_movement_options() + [None])


def test_choose_next_move_no_stay(mocker, setup_rooms_and_visitor):
	visitor = setup_rooms_and_visitor

	mocker.patch('random.random', return_value=0.9)

	chosen_sensors = {choose_next_move(visitor) for _ in range(100)}

	# Ensure the visitor moves to one of the available sensors
	assert chosen_sensors.issubset(set(visitor.get_movement_options()))

	# Check if the visitor never stayed in the same room (so it should have moved)
	assert None not in chosen_sensors


def test_choose_next_move_stay(mocker, setup_rooms_and_visitor):
	visitor = setup_rooms_and_visitor

	mocker.patch('random.random', return_value=0.05)

	chosen_sensors = {choose_next_move(visitor) for _ in range(100)}

	# Ensure the visitor stays in the same room each time
	assert chosen_sensors.issubset({None})


def test_choose_next_move_no_options(visitor):
	# Create a mock visitor with no movement options
	visitor.get_movement_options = lambda: []

	# Expect an exception when no movement options are available
	with pytest.raises(Exception, match='No movement options found for visitor:'):
		choose_next_move(visitor)


def test_get_weights(visitor, rooms):
	# Mock the movement options to have two sensors
	visitor.get_movement_options = lambda: [Sensor(1, []), Sensor(2, [rooms[0], rooms[2]])]
	print(get_weights(visitor.get_movement_options(), visitor))
	# Ensure the function returns a list of floats
	assert all(
		isinstance(weight, (float, int))
		for weight in get_weights(visitor.get_movement_options(), visitor)
	)

	# Ensure the function returns a list of the same length as the movement options
	assert len(get_weights(visitor.get_movement_options(), visitor)) == len(
		visitor.get_movement_options()
	)

	# Ensure the function returns a list of weights between 0 and 1
	assert all(0 <= weight <= 1 for weight in get_weights(visitor.get_movement_options(), visitor))


def test_should_create_visitor():
	# Run the function multiple times to check randomness
	created_visitors = [should_create_visitor() for _ in range(100)]

	# Ensure the function returns a boolean
	assert all(isinstance(visitor, bool) for visitor in created_visitors)

	# Ensure the function returns True with a probability of 0.2
	assert sum(created_visitors) / len(created_visitors) == pytest.approx(0.2, abs=0.1)


def test_should_create_visitor_fixed(mocker):
	# Mock the random function to always return 0.1
	mocker.patch('random.random', return_value=0.1)

	# Expect the function to return True
	assert should_create_visitor()

	# Mock the random function to always return 0.9
	mocker.patch('random.random', return_value=0.9)

	# Expect the function to return False
	assert not should_create_visitor()
