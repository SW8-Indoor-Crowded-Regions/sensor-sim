import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import bson
from app.main import app
from fastapi import HTTPException
from unittest.mock import AsyncMock

client = TestClient(app)

@pytest.fixture
def sample_room():
    return {
        "id": str(bson.ObjectId()),
        "name": "Test Room",
        "type": "MEETING",
        "crowd_factor": 0.8,
        "occupants": 10,
        "area": 25.5,
        "longitude": 40.7128,
        "latitude": -74.0060,
    }

@pytest.mark.asyncio
@patch("app.routes.rooms.get_all_rooms", new_callable=AsyncMock)
async def test_fetch_rooms(mock_get_all_rooms, sample_room):
    mock_get_all_rooms.return_value = [sample_room, sample_room]

    response = client.get("/rooms/")

    assert response.status_code == 200
    assert response.json() == {"rooms": [sample_room, sample_room]}

@patch("app.routes.rooms.get_all_rooms")
def test_fetch_rooms_empty(mock_get_all_rooms):
    mock_get_all_rooms.return_value = []
    response = client.get("/rooms/")
    assert response.status_code == 200
    assert response.json() == {"rooms": []}

@patch("app.routes.rooms.get_room_by_id")
def test_fetch_room_by_id(mock_get_room_by_id, sample_room):
    mock_get_room_by_id.return_value = sample_room
    response = client.get(f"/rooms/{sample_room['id']}")
    assert response.status_code == 200
    assert response.json() == sample_room

@patch("app.routes.rooms.get_room_by_id")
def test_fetch_room_by_id_not_found(mock_get_room_by_id):
    mock_get_room_by_id.side_effect = HTTPException(status_code=404, detail="Room not found.")
    response = client.get(f"/rooms/{bson.ObjectId()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Room not found."

@patch("app.routes.rooms.get_room_by_id")
def test_fetch_room_by_id_invalid_id(mock_get_room_by_id):
    mock_get_room_by_id.side_effect = HTTPException(status_code=400, detail="Invalid room id.")
    response = client.get("/rooms/invalid_id")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid room id."
