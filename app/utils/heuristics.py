import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from app.classes.visitor import Visitor
	from app.classes.sensor import Sensor


def choose_next_move(visitor: 'Visitor') -> 'Sensor | None':
	"""Chooses the next move for the visitor.

	Returns:
			Sensor: The sensor that the visitor will move through.
	"""
	movement_options = visitor.get_movement_options()

	if not movement_options:
		raise Exception('No movement options found for visitor:', visitor.__str__())

	# Chance to stay in the same room
	stay_probability = visitor.get_current_room().popularity_factor * 0.1
	if random.random() < stay_probability:
		return None

	weights = get_weights(movement_options, visitor)

	# Normalize weights
	total_weight = sum(weights)
	normalized_weights = [weight / total_weight for weight in weights]

	# Choose a random sensor to move to. Chance should be lower for sensor leeding to previous room
	return random.choices(movement_options, normalized_weights)[0]


def get_weights(movement_options: list['Sensor'], visitor: 'Visitor') -> list[float]:
	"""Returns the weights for each movement option.

	Args:
			movement_options (list[Sensor]): The movement options for the visitor.
			visitor (Visitor): The visitor.
	Returns:
			list[float]: The weights for each movement option.
	"""
	weights: list[float] = []
	previous_room_id: int | None = (
		visitor.visited_rooms[-2].id if len(visitor.visited_rooms) > 1 else None
	)
	for sensor in movement_options:
		if previous_room_id and previous_room_id in [room.id for room in sensor.rooms]:
			weights.append(0.1)
		else:
			weights.append(1)
	return weights


def should_create_visitor() -> bool:
	"""Returns a boolean indicating whether a visitor should be created.

	Returns:
			bool: True if a visitor should be created, False otherwise.
	"""
	return random.random() < 0.5
