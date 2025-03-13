import bson.errors
from fastapi import HTTPException
from db.models.room import Room
from app.utils.data_models.rooms import RoomModel
import bson 


async def get_all_rooms() -> list[RoomModel]:
	"""Fetch all rooms from the database."""
	try:
		rooms = Room.objects()  # type: ignore
		return list(rooms)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


async def get_room_by_id(room_id: str) -> RoomModel:
	"""Fetch a room by its id."""
	validate_room_id(room_id)
	try:
		room = await fetch_room_by_id(room_id)
		return room
	except HTTPException:
		raise
	except Exception as e:
		print(e)
		raise HTTPException(status_code=500, detail=str(e))


def validate_room_id(room_id: str):
	if not bson.ObjectId.is_valid(room_id):
		raise HTTPException(status_code=400, detail='Invalid room id.')


async def fetch_room_by_id(room_id: str) -> RoomModel:
	room = Room.objects(id=bson.ObjectId(room_id)).first()  # type: ignore
	if not room:
		raise HTTPException(status_code=404, detail='Room not found.')
	return room
