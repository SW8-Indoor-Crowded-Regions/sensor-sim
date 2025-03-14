from app.classes.room import Room
from mongoengine import get_db
from pymongo import UpdateOne

def save_data(rooms: list[Room]) -> None:
	"""Save the data to the database."""
	db = get_db()
	room_collection = db['rooms']
	
	bulk_operations = [
		UpdateOne(
			{'_id': room.id},
			{'$set': {"occupants": room.occupancy}},
			upsert=True,
		)
		for room in rooms
	]
 
	if bulk_operations:
		room_collection.bulk_write(bulk_operations)
  
	print('Data saved to the database.')