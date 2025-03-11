import pytest
from kafka import KafkaConsumer
from app.classes.consumer import Consumer

@pytest.fixture
def mock_kafka_consumer(monkeypatch):
  class MockKafkaConsumer:
    def __init__(self, *args, **kwargs):
      self.messages = []
      self.poll_timeout = None

    def __iter__(self):
      return iter(self.messages)

    def poll(self, timeout_ms):
      self.poll_timeout = timeout_ms
      return {}

  monkeypatch.setattr(KafkaConsumer, "__init__", MockKafkaConsumer.__init__)
  monkeypatch.setattr(KafkaConsumer, "__iter__", MockKafkaConsumer.__iter__)
  monkeypatch.setattr(KafkaConsumer, "poll", MockKafkaConsumer.poll)
  return MockKafkaConsumer()

def test_consume_messages(mock_kafka_consumer, monkeypatch):
  def mock_process_function(message):
    assert message == {"key": "value"}

  consumer = Consumer(mock_process_function, "test_topic")
  mock_kafka_consumer.messages = [{"value": {"key": "value"}}]

  consumer.consume_messages()