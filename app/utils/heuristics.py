import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from app.classes.visitor import Visitor
	from app.classes.sensor import Sensor

# Immutable values with less boilerplate
@dataclass(frozen=True)
class MovementConfig:
    alpha: float = 0.1
    beta: float = 0.1
    penalty_factor: float = 0.1
    create_visitor_probability: float = 0.1
        

def choose_next_move(visitor: 'Visitor', config: MovementConfig) -> 'Sensor | None':
	"""Chooses the next move for the visitor.
	Returns:
		Sensor: The sensor that the visitor will move through.
	"""
	movement_options = visitor.get_movement_options()
	if not movement_options:
		raise Exception(f'No movement options found for visitor: {visitor}')

	# Chance to stay in the same room
	stay_probability = p_stay(visitor, config.alpha, config.beta)
	if random.random() < stay_probability:
		return None

	weights = get_weights(movement_options, visitor, config.penalty_factor)
	normalized_weights = normalize_weights(weights)

	# Choose a random sensor to move to. Chance should be lower for sensor leeding to previous room
	return random.choices(movement_options, normalized_weights)[0]


def get_weights(
	movement_options: list['Sensor'], visitor: 'Visitor', penalty_factor: float
) -> list[float]:
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
		if previous_room_id and any(room.id == previous_room_id for room in sensor.rooms):
			popularity_factor = visitor.get_current_room().popularity_factor
			weights.append(popularity_factor * penalty_factor)
		else:
			weights.append(1)
	return weights


def should_create_visitor(config: MovementConfig) -> bool:
	"""Returns a boolean indicating whether a visitor should be created.

	Returns:
			bool: True if a visitor should be created, False otherwise.
	"""
	return random.random() < config.create_visitor_probability


def p_stay(visitor: 'Visitor', alpha: float, beta: float) -> float:
	"""Calculates the stay_probability"""

	# Fixed bounds for normalization
	MAX_POPULARTIY = 2.0 	# highest popularity factor
	MAX_AREA = 2916 	# Skulpturgaden is the largest area with 2915.98 square meters

	popularity = visitor.get_current_room().popularity_factor
	area = visitor.get_current_room().area

	normalized_popularity = popularity / MAX_POPULARTIY
	normalized_area = area / MAX_AREA  

	stay_probability = (alpha * normalized_popularity) + (beta * normalized_area)
	return max(0.0, min(stay_probability, 1.0))


def normalize_weights(weights: list[float]) -> list[float]:
	"""Returns a list of the normalized weights"""
	total_weight = sum(weights)
	if total_weight == 0:
		raise Exception('Sum of weights cannot be zero, as this leads to zero division')
	return [weight / total_weight for weight in weights]
