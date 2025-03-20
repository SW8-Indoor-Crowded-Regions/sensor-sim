import uvicorn
from fastapi import FastAPI
from app.routes import rooms
from app.routes import sensors
from db.database import Database
from app.utils.data_models.general import HealthCheckModel
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI): # pragma: no cover
	Database()
	yield


app = FastAPI(
	title='Room Occupancy API',
	description="""API for retrieving room and sensor data. 
	The API is used to retrieve data about rooms and sensors in a Statens Museum for Kunst (SMK), Copenhagen, Denmark. 
	The data is used to calculate the crowd factor in each room.""",
	version='0.1.0',
	docs_url='/docs',
	redoc_url='/redoc',
	lifespan=lifespan,
)

app.include_router(rooms.router)
app.include_router(sensors.router)


@app.get(
	'/health',
	tags=['Health'],
	response_model=HealthCheckModel,
	description='Health check endpoint. Returns the status of the API.',
	response_description='A dictionary containing the status of the API.',
	summary='Health check',
	response_model_exclude_unset=True,
)
async def health_check():
	"""Health check endpoint.
	Returns:
		dict: A dictionary containing the status of the API.
	"""
	return {'status': 'ok'} # pragma: no cover


if __name__ == '__main__':
	uvicorn.run('main:app', host='0.0.0.0', port=8002, reload=True)
