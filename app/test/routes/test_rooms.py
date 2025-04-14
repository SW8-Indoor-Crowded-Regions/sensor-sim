import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import bson
from app.main import app
from fastapi import HTTPException
from unittest.mock import AsyncMock
from app.test.factories.room_factory import RoomFactory

client = TestClient(app)



@pytest.mark.asyncio
@patch('app.routes.rooms.get_all_rooms', new_callable=AsyncMock)
async def test_fetch_rooms(mock_get_all_rooms):
	exp_rooms = [RoomFactory(name="Room " + str(i)).to_dict() for i in range(10)]
	mock_get_all_rooms.return_value = exp_rooms

	response = client.get('/rooms/')

	assert response.status_code == 200
	assert response.json() == {'rooms': exp_rooms}


@patch('app.routes.rooms.get_all_rooms')
def test_fetch_rooms_empty(mock_get_all_rooms):
	mock_get_all_rooms.return_value = []
	response = client.get('/rooms/')
	assert response.status_code == 200
	assert response.json() == {'rooms': []}


@patch('app.routes.rooms.get_room_by_id')
def test_fetch_room_by_id(mock_get_room_by_id):
	exp_room = RoomFactory()
	mock_get_room_by_id.return_value = exp_room
	response = client.get(f'/rooms/{exp_room.id}')
	assert response.status_code == 200
	assert response.json() == exp_room.to_dict()


@patch('app.routes.rooms.get_room_by_id')
def test_fetch_room_by_id_not_found(mock_get_room_by_id):
	mock_get_room_by_id.side_effect = HTTPException(status_code=404, detail='Room not found.')
	response = client.get(f'/rooms/{bson.ObjectId()}')
	assert response.status_code == 404
	assert response.json()['detail'] == 'Room not found.'


@patch('app.routes.rooms.get_room_by_id')
def test_fetch_room_by_id_invalid_id(mock_get_room_by_id):
	mock_get_room_by_id.side_effect = HTTPException(status_code=400, detail='Invalid room id.')
	response = client.get('/rooms/invalid_id')
	assert response.status_code == 400
	assert response.json()['detail'] == 'Invalid room id.'
