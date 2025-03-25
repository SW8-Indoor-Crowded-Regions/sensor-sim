from db import Database
from app.data_processing.data_processing import process_sensor_data
from app.utils.load_objects import load_rooms

def main():
	Database()
	rooms = load_rooms()
	process_sensor_data(rooms)
 
if __name__ == '__main__':
	main()