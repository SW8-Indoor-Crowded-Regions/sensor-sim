import pytest
import json
from app.classes.consumer import Consumer
from app.classes.room import Room


@pytest.fixture
def mock_env(monkeypatch):
	"""Mock environment variables."""
	monkeypatch.setenv('KAFKA_BROKER', 'localhost:9092')


@pytest.fixture
def mock_kafka_consumer(mocker):
	"""Mock KafkaConsumer as an iterable list of messages."""
	mock_consumer = mocker.MagicMock()

	# Define sample messages
	mock_messages = [
		mocker.Mock(value=json.dumps({'msg': 1}).encode('utf-8')),
		mocker.Mock(value=json.dumps({'msg': 2}).encode('utf-8')),
	]

	# Make the consumer iterable like a list
	mock_consumer.__iter__.return_value = iter(mock_messages)

	return mock_consumer


@pytest.fixture
def consumer(mock_env, mock_kafka_consumer, mocker, monkeypatch):
	"""Initialize Consumer and replace its KafkaConsumer instance with a mock."""
	monkeypatch.setattr('app.classes.consumer.KafkaConsumer', mocker.Mock())
	mock_process_function = mocker.Mock(return_value=("mock_sensor_id", []))  # Fix: Returns tuple

	consumer_instance = Consumer(mock_process_function, 'test-topic')
	consumer_instance.consumer = mock_kafka_consumer  # Override with mock
	return consumer_instance


def test_init(mocker, monkeypatch):
	mock_kafka = mocker.Mock()
	monkeypatch.setattr('app.classes.consumer.KafkaConsumer', mock_kafka)
	mock_process_function = mocker.Mock()

	consumer = Consumer(mock_process_function, 'sensor-data')
	assert consumer.topic == 'sensor-data'
	assert consumer.process_function == mock_process_function
	assert mock_kafka.called
	assert mock_kafka.return_value.subscribe.called_with('sensor-data')


def test_consume_messages(consumer, monkeypatch):
	monkeypatch.setattr('app.classes.consumer.KafkaConsumer', consumer.consumer)
	consumer.consume_messages()

	assert consumer.process_function.call_count == 2


def test_consume_messages_no_messages(consumer, mocker, monkeypatch):
	"""Test that consume_messages() does not call process_function when no messages are received."""
	mock_kafka = mocker.MagicMock()
	monkeypatch.setattr('app.classes.consumer.KafkaConsumer', mock_kafka)
	consumer.consumer = mock_kafka

	consumer.consume_messages()
	assert consumer.process_function.call_count == 0
