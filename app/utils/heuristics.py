import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from app.classes.visitor import Visitor
	from app.classes.sensor import Sensor

def choose_next_move(visitor: "Visitor") -> "Sensor":
	"""Chooses the next move for the visitor.

	Returns:
			Sensor: The sensor that the visitor will move through.
	"""

	current_room = visitor.get_current_room()

	movement_options = visitor.get_movement_options()


	if not movement_options:
		raise Exception("No movement options found for visitor:", visitor)

	# Choose a random sensor to move to
	return random.choice(movement_options)