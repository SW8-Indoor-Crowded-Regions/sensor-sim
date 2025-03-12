from app.utils.kafka_producer import send_data


def test_send_data(mocker):
	data = {"id": 1, "rooms": [1, 2], "movements": [0, 0]}
	mock_producer = mocker.patch('app.utils.kafka_producer.KafkaProducer')
 
	send_data(data)
	# Assert that flush() was called
	mock_producer.return_value.send.assert_called_once_with("sensor-data", value=data)

def test_send_empty_data(mocker):
	data = {}
	mock_producer = mocker.patch('app.utils.kafka_producer.KafkaProducer')
 
	send_data(data)
	# Assert that flush() was called
	mock_producer.return_value.send.assert_called_once_with("sensor-data", value=data)