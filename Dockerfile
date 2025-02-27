FROM python:3.11
WORKDIR /kafka-test
COPY . /kafka-test/
RUN pip install kafka-python
CMD ["python", "kafkaProducer.py"]