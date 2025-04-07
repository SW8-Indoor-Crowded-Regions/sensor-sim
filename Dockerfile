# Use Python 3.11 slim image
FROM python:3.11.9-slim

# Install necessary dependencies (git for version control, curl for downloading wait-for-it.sh)
RUN apt-get update && \
    apt-get install -y git curl && \
    rm -rf /var/lib/apt/lists/*

# Download wait-for-it.sh script using curl
RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /wait-for-it.sh

# Make sure the script is executable
RUN chmod +x /wait-for-it.sh

# Set the working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy entrypoint script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh
# Expose the port the app will run on
EXPOSE 8002

# Command to wait for Kafka and Zookeeper before starting the app
CMD ["/wait-for-it.sh", "kafka:9092", "--", "./start.sh"]
