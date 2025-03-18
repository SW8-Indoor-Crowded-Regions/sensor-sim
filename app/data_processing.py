import sys
import os
from db import Database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_processing.crowd_factor import process_sensor_data
from app.utils.load_objects import load_rooms

Database()

rooms = load_rooms()

process_sensor_data(rooms)