get_sensor_by_id_responses: dict[int | str, dict[str, object]] = {
  200: {
    'description': 'Successful Response',
    'content': {
      'application/json': {'example': {'id': '123', 'rooms': ['Room 1'], 'movements': [1]}}
    },
  },
  400: {
    'description': 'Invalid Sensor ID',
    'content': {'application/json': {'example': {'detail': 'Invalid Sensor ID'}}},
  },
  404: {
    'description': 'Sensor not found',
    'content': {'application/json': {'example': {'detail': 'Sensor not found'}}},
  },
  500: {
    'description': 'Internal Server Error',
    'content': {'application/json': {'example': {'detail': 'Internal Server Error'}}},
  }
}

get_sensors_responses: dict[int | str, dict[str, object]] = {
  200: {
		'description': 'Successful Response',
		'content': {
			'application/json': {
				'example': [
					{'id': '123', 'rooms': ['Room 1'], 'movements': [1]},
          {'id': '124', 'rooms': ['Room 2'], 'movements': [2]},
				]
			}
		},
	},
	500: {
		'description': 'Internal Server Error',
		'content': {'application/json': {'example': {'detail': 'Internal Server Error'}}},
	}
}