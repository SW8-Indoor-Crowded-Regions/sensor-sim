from db.models.room import Room
from db.models.sensor import Sensor
from db.database import Database
import random

db = Database()

# Example adjacency (doors/openings) for the middle rooms from the floor plan.
# Extend as needed for the rest of the rooms on your floor plan.
ROOM_ADJACENCY = {
	# ------------ first floor ------------
	# -- ring wing --
	'RW1': ['T2', 'T3', 'KAFETERIA', '101', '107'],
	'KAFETERIA': ['RW1', 'HALL'],
	'107': ['RW1', '106'],
	'106': ['107', '105'],
	'105': ['104', '106'],
	'104': ['103', '105'],
	'103': ['102', '104'],
	'102': ['103', 'HALL'],
	'101': ['RW1', 'HALL'],
	# -- middle --
	'HALL': ['T1'],
	# -- left wing --
	'109': ['HALL', 'LW1'],
	'108': ['HALL', 'LW1'],
	'SHOP': ['HALL', 'LW1'],
	'LW1': ['108', '109', 'SHOP'],
	# -- left new building
	'114': [
		'115',
	],
	'115': ['113', '114', 'STAGE'],
	'117': ['STAGE'],
	# -- middle new building --
	'STAGE': ['113', '115', 'AUDITORIUM', '117'],
	'113': ['HALL', 'AUDITORIUM', 'STAGE', '115'],
	# -- right new building
	'AUDITORIUM': ['113', 'STUDYROOM', 'STAGE'],
	'STUDYROOM': ['T4', 'AUDITORIUM', '113'],
	# ------------ second floor ------------
	# -- Ring wing 2nd floor--
	'201A': ['201B', '211B', '202', 'P1'],
	'201B': ['201A', '201C'],
	'201C': ['201B', '201D'],
	'201D': ['201E', '209'],
	'201E': ['201D', '204'],
	'202': ['203', '201A', 'P1'],
	'203': ['202', '204'],
	'204': ['203', '201E', '205'],
	'211B': ['201A', '211A'],
	'211A': ['211B', '210B'],
	'210B': ['211A', '210A'],
	'210A': ['209', '210B'],
	'208B': ['209', '208A', '205'],
	'209': ['210A', '208B', '201D'],
	'208A': ['208B', '207'],
	'207': ['208A', '206', 'T2', 'T3'],
	'206': ['207', '205'],
	'205': ['206', '204', '208B', '208A'],
	'T2': ['207', 'RW1'],
	'T3': ['207', 'RW1'],
	# -- middle passage etc --
	'P1': ['201A', '202', '212', 'P2', 'P3'],  # right side of the hall 2nd floor
	'P2': ['P1', 'P4'],  # upper middle of hall 2nd floor
	'P3': ['P1', 'P4'],  # lower middle of hall 2nd floor
	'P4': ['P3', 'P2', '229', '217A', '216'],  # left side of hall 2nd floor
	'212': ['P1', '213'],
	'213': ['212', '214'],
	'214': ['213', '215'],
	'215': ['214', '216'],
	'216': ['P4', '215'],
	'T1': ['HALL', 'P1'],
	# -- left wing --
	'217A': ['218A', '229', '217B', 'P4'],
	'229': ['217A', 'P4', '228'],
	'228': ['229', '227'],
	'227': ['228', '217F', '221'],
	'217F': ['217E', '220', '227'],
	'217E': ['217F', '217D'],
	'217D': ['217E', '217C'],
	'217C': ['217D', '217B'],
	'217B': ['217C', '217A'],
	'218A': ['218B', '217A'],
	'218B': ['218A', '219'],
	'219': ['218B', '220'],
	'220': ['219', '217F', 'P7'],
	'P7': ['220', '221', '222'],
	'222': ['P7', '223'],
	'223': ['221', '222', '224'],
	'224': ['223', '225'],
	'225': ['226', '221', '224'],
	'221': ['P7', '225', '223', '227'],
	'226': ['225'],
	# -- left new building --
	'P5': ['218A', 'P8', 'P9'],
	'P8': ['270B', '270A', '262', '272', '261', 'P5'],
	'T7': ['115', 'P8'],
	'T6': ['P5', '113'],
	'270B': ['P8'],
	'270A': ['P8'],
	'262': ['P8', '261'],
	'261': ['P8', '262'],
	'272': ['P8', '260'],
	'260': ['272'],
	# -- middle new building --
	'P9': ['269A', '269B', '263B', '263C', 'P6', 'P5'],
	'269A': ['P9'],
	'269B': ['P9'],
	'263B': ['263C', 'P9'],
	'263C': ['P9', '263B', '263A'],
	'263A': ['263C'],
	# -- right new building
	'P6': ['P9', 'P10', '211B'],
	'P10': ['P6', '268A', '268B', '264', '267', '265', '266'],
	'T5': ['P6', '113'],
	'T4': ['P10', 'STUDYROOM'],
	'268A': ['P10'],
	'268B': ['P10'],
	'264': ['P10', '264A'],
	'264A': ['264'],
	'267': ['P10'],
	'265': ['P10', '266'],
	'266': ['P10', '265'],
}


def rand_beta_dist() -> float:
	"""
	Generate a float value between 0.2 and 2, with emphasis between 0.5 and 1.5, Using a beta distribution.
	Returns:
	    float: A value between 0.2 and 2
	"""
	return max(0.2, random.betavariate(5, 5) * 2)


def create_rooms_and_sensors():
	"""
	Creates Room documents for each labeled room in ROOM_ADJACENCY,
	and creates Sensor documents for each doorway/opening between rooms.
	"""

	# Empty the database
	Room.objects.delete()  # type: ignore
	Sensor.objects.delete()  # type: ignore

	# Dictionary to store {room_name: Room_object} after creation
	room_objects = {}

	# 1) Create Room objects in the database
	for room_name in ROOM_ADJACENCY.keys():
		# Example dummy data - adjust as needed
		room = Room(
			name=room_name,
			type='EXHIBITION',  # or LOBBY, OFFICE, etc.
			crowd_factor=rand_beta_dist(),
			popularity_factor=rand_beta_dist(),
			area=50.0,  # dummy area
			longitude=0.0,  # dummy coordinates
			latitude=0.0,
		).save()

		room_objects[room_name] = room

	# 2) Create Sensor objects for each pair of adjacent rooms
	#    We'll keep track of pairs we've already processed to avoid duplicates.
	created_pairs = set()
	for room_name, neighbors in ROOM_ADJACENCY.items():
		for neighbor_name in neighbors:
			# Sort the pair so (201B, 201C) is the same as (201C, 201B)
			pair = tuple(sorted([room_name, neighbor_name]))

			if pair not in created_pairs:
				sensor_name = f'Sensor_{pair[0]}_{pair[1]}'
				sensor = Sensor(
					name=sensor_name, rooms=[room_objects[pair[0]], room_objects[pair[1]]]
				)
				sensor.save()

				created_pairs.add(pair)

	print('Rooms and sensors created successfully!')


create_rooms_and_sensors()
