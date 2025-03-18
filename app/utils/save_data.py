from app.classes.room import Room
from mongoengine import get_db
from pymongo import UpdateOne


def save_data(rooms: list[Room]) -> None:
	"""Save the data to the database."""
	db = get_db()
	room_collection = db['room']

	bulk_operations = [
		UpdateOne(
			{'_id': room.id},
			{'$set': {'occupants': room.occupancy}},
			upsert=True,
		)
		for room in rooms
	]

	if bulk_operations:
		update = room_collection.bulk_write(bulk_operations)
		print(f'Updated {update.modified_count} rooms.')
	else:
		print('No data to save.')