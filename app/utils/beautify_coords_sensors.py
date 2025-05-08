from collections import defaultdict
from copy import deepcopy
import json

# Example margin in degrees (~1 meter): adjust based on your required precision
COORD_MARGIN = 0.00001

def within_margin(val1, val2, margin=COORD_MARGIN):
    return abs(val1 - val2) <= margin

def normalize_sensor_coordinates(sensors):
    # Map room IDs to list of sensor indices
    room_to_sensors = defaultdict(list)
    for i, sensor in enumerate(sensors):
        for room in sensor['rooms']:
            room_to_sensors[room['$oid']].append(i)

    sensors_updated = deepcopy(sensors)

    for sensor_indices in room_to_sensors.values():
        for i in range(len(sensor_indices)):
            base_idx = sensor_indices[i]
            base = sensors[base_idx]

            base_lat = base['latitude']
            base_lon = base['longitude']

            for j in range(i + 1, len(sensor_indices)):
                other_idx = sensor_indices[j]
                other = sensors_updated[other_idx]

                # Compare latitude
                if within_margin(base_lat, other['latitude']) and not within_margin(base_lon, other['longitude']):
                    other['latitude'] = base_lat
                # Compare longitude
                if within_margin(base_lon, other['longitude']) and not within_margin(base_lat, other['latitude']):
                    other['longitude'] = base_lon
                # If both are within margin, set both
                if within_margin(base_lat, other['latitude']) and within_margin(base_lon, other['longitude']):
                    other['latitude'] = base_lat
                    other['longitude'] = base_lon

    return sensors_updated
 
if __name__ == "__main__":
	with open('data/sensors_copy.json', 'r') as file:
		sensors = json.load(file)
	normalized_sensors = normalize_sensor_coordinates(sensors)
	with open('data/sensors_copy.json', 'w') as file:
		json.dump(normalized_sensors, file, indent=4)
		print("Normalized sensors saved to 'data/sensors_copy.json'")