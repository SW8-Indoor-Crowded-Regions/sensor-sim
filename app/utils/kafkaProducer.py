from kafka import KafkaProducer
import json
import time
import os
import random
from sensorDataSim import initSensors, intervalMovement

# Kafka setup
KAFKA_TOPIC = "sensor-data"
KAFKA_BROKER = "localhost:9092"

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
						 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

	
# Simulating multiple sensors
current_dir = os.path.dirname(os.path.abspath(__file__))
sensors_file_path = os.path.join(current_dir, "sensors", "sensors.json")

sensors, rooms = initSensors()
timeStamp = 0

try:
	while True:
		sensors = intervalMovement(sensors, timeStamp)
		timeStamp+=1
		for room in rooms.values():
			producer.send(KAFKA_TOPIC, value=room.getOccupancy())
			print(f"Sent: {room.getOccupancy()}")
  
		"""for sensor_id in sensors:
			sensor_data = random.choices(
				range(5),
				weights=[0.8, 0.1, 0.05, 0.035, 0.015]
			)[0]
			producer.send(KAFKA_TOPIC, value=sensor_data)
			print(f"Sent: {sensor_data}")"""
		time.sleep(1)
except KeyboardInterrupt as e:
	print("\nProducer closing...")
finally:
	producer.flush()
	producer.close()
	print("Producer closed.")