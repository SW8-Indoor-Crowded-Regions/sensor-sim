# Use Python 3.11 slim image
FROM python:3.11.9-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy entrypoint script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose the port the app will run on
EXPOSE 8002

# Command to wait for Kafka and Zookeeper before starting the app
CMD ["/start.sh"]
