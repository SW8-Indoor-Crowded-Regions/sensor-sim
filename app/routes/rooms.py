from fastapi import APIRouter
from app.controllers.room_controller import get_all_rooms, get_room_by_id
from app.utils.data_models.rooms import RoomListModel, RoomModel
from app.utils.response_examples.rooms import get_room_by_id_responses, get_rooms_responses

router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.get(
	'', #path here set to /rooms as default
	response_model=RoomListModel,
	summary='Get all rooms',
	tags=['Rooms'],
	response_description='Returns a list of all rooms.',
	description='Get all rooms from the database.',
	response_model_exclude_unset=True,
	responses=get_rooms_responses
)
async def fetch_rooms():
	"""Get all rooms.
	Returns:
	  dict: A dictionary containing a list of rooms.
	"""
	rooms = get_all_rooms()
	return {'rooms': await rooms}


@router.get(
	'/{room_id}',
	response_model=RoomModel,
	summary='Get room by id',
	tags=['Rooms'],
	response_description='Returns a room by its id.',
	description='Get a room by its id.',
	response_model_exclude_unset=True,
	responses=get_room_by_id_responses,
)
async def fetch_room_by_id(room_id: str) -> RoomModel:
	"""Get a room by its id.
	Args:
	  room_id (str): The id of the room.
	Returns:
	  dict: A dictionary containing the room.
	"""
	room = get_room_by_id(room_id)
	return await room
