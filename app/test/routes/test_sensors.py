import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import bson
from app.main import app
from fastapi import HTTPException

client = TestClient(app)

@pytest.fixture
def sample_sensor():
    return {
        "id": str(bson.ObjectId()),
        "rooms": [str(bson.ObjectId())],
    }

@pytest.mark.asyncio
@patch("app.routes.sensors.get_all_sensors", new_callable=AsyncMock)
async def test_fetch_sensors(mock_get_all_sensors, sample_sensor):
	"""Test GET /sensors"""
	mock_get_all_sensors.return_value = [sample_sensor, sample_sensor]

	response = client.get("/sensors/")

	assert response.status_code == 200
	assert response.json() == {"sensors": [sample_sensor, sample_sensor]}

@patch("app.routes.sensors.get_all_sensors")
def test_fetch_sensors_empty(mock_get_all_sensors):
    """Test GET /sensors when no sensors exist"""
    mock_get_all_sensors.return_value = []

    response = client.get("/sensors/")

    assert response.status_code == 200
    assert response.json() == {"sensors": []}

@patch("app.routes.sensors.get_all_sensors")
def test_fetch_sensors_error(mock_get_all_sensors):
    """Test GET /sensors when an error occurs"""
    mock_get_all_sensors.side_effect = HTTPException(status_code=500, detail="Database error")

    response = client.get("/sensors/")

    assert response.status_code == 500
    assert response.json()["detail"] == "Database error"

@patch("app.routes.sensors.get_sensor_by_id")
def test_fetch_sensor_by_id(mock_get_sensor_by_id, sample_sensor):
    """Test GET /sensors/{sensor_id}"""
    mock_get_sensor_by_id.return_value = sample_sensor

    response = client.get(f"/sensors/{sample_sensor['id']}")

    assert response.status_code == 200
    assert response.json() == sample_sensor

@patch("app.routes.sensors.get_sensor_by_id")
def test_fetch_sensor_by_id_not_found(mock_get_sensor_by_id):
    """Test GET /sensors/{sensor_id} when sensor is not found"""
    mock_get_sensor_by_id.side_effect = HTTPException(status_code=404, detail="Sensor not found.")

    response = client.get(f"/sensors/{bson.ObjectId()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor not found."

@patch("app.routes.sensors.get_sensor_by_id")
def test_fetch_sensor_by_id_invalid(mock_get_sensor_by_id):
    """Test GET /sensors/{sensor_id} with invalid ID format"""
    mock_get_sensor_by_id.side_effect = HTTPException(status_code=400, detail="Invalid sensor id.")

    response = client.get("/sensors/invalid_id")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid sensor id."
