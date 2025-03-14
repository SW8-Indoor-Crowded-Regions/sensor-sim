import pytest
from fastapi import HTTPException
from unittest.mock import patch
import bson
from db.models.room import Room
from app.controllers.room_controller import (
	get_all_rooms,
	get_room_by_id,
	validate_room_id,
	fetch_room_by_id,
)


# Sample room data
def sample_room() -> Room:
	return Room(
		id=bson.ObjectId(),
		name='Room A',
		type='LOBBY',
		crowd_factor=1.0,
		area=30,
		longitude=40.0,
		latitude=-73.0,
	)


@pytest.fixture
def mock_rooms():
	return [
		Room(
			id=bson.ObjectId(),
			name='Room A',
			type='LOBBY',
			crowd_factor=1.0,
			area=30,
			longitude=40.0,
			latitude=-73.0,
		),
		Room(
			id=bson.ObjectId(),
			name='Room B',
			type='OFFICE',
			crowd_factor=0.5,
			area=20,
			longitude=41.0,
			latitude=-72.0,
		),
	]


@patch('db.models.room.Room.objects')
@pytest.mark.asyncio
async def test_get_all_rooms(mock_objects, mock_rooms):
	mock_objects.return_value = mock_rooms
	rooms = await get_all_rooms()
	assert len(rooms) == len(mock_rooms)
	assert all(isinstance(room, Room) for room in rooms)


@patch('db.models.room.Room.objects')
@pytest.mark.asyncio
async def test_get_all_rooms_exception(mock_objects):
	mock_objects.side_effect = Exception('Database error')
	with pytest.raises(HTTPException) as exc:
		await get_all_rooms()
	assert exc.value.status_code == 500
	assert 'Database error' in exc.value.detail


@pytest.mark.parametrize(
	'room_id, is_valid',
	[
		(str(bson.ObjectId()), True),
		('invalid_id', False),
		('1234567890abcdef12345678', True),
		('12345', False),
	],
)
def test_validate_room_id(room_id, is_valid):
	if is_valid:
		validate_room_id(room_id)  # Should not raise an exception
	else:
		with pytest.raises(HTTPException) as exc:
			validate_room_id(room_id)
		assert exc.value.status_code == 400
		assert 'Invalid room id' in exc.value.detail


@patch('db.models.room.Room.objects')
@pytest.mark.asyncio
async def test_fetch_room_by_id_found(mock_objects):
	room = sample_room()
	mock_objects.return_value.first.return_value = room
	result = await fetch_room_by_id(str(room.id)) # type: ignore
	assert result == room


@patch('db.models.room.Room.objects')
@pytest.mark.asyncio
async def test_fetch_room_by_id_not_found(mock_objects):
	mock_objects.return_value.first.return_value = None
	with pytest.raises(HTTPException) as exc:
		await fetch_room_by_id(str(bson.ObjectId()))
	assert exc.value.status_code == 404
	assert 'Room not found' in exc.value.detail


@patch('app.controllers.room_controller.fetch_room_by_id')
@pytest.mark.asyncio
async def test_get_room_by_id_success(mock_fetch_room):
	room = sample_room()
	mock_fetch_room.return_value = room
	result = await get_room_by_id(str(room.id)) # type: ignore
	assert result == room


@patch('app.controllers.room_controller.fetch_room_by_id')
@pytest.mark.asyncio
async def test_get_room_by_id_not_found(mock_fetch_room):
	mock_fetch_room.side_effect = HTTPException(status_code=404, detail='Room not found.')
	with pytest.raises(HTTPException) as exc:
		await get_room_by_id(str(bson.ObjectId()))
	assert exc.value.status_code == 404
	assert 'Room not found' in exc.value.detail


@patch('app.controllers.room_controller.fetch_room_by_id')
@pytest.mark.asyncio
async def test_get_room_by_id_internal_server_error(mock_fetch_room):
	mock_fetch_room.side_effect = Exception('Unexpected error')
	with pytest.raises(HTTPException) as exc:
		await get_room_by_id(str(bson.ObjectId()))
	assert exc.value.status_code == 500
	assert 'Unexpected error' in exc.value.detail
