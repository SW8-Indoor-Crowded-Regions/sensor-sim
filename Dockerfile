# Use Python 3.11 slim image
FROM python:3.11.9-slim

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y git curl && \
    rm -rf /var/lib/apt/lists/*

# Download wait-for-it.sh
RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /wait-for-it.sh && \
    chmod +x /wait-for-it.sh

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code *before* you copy start.sh (to avoid overwriting it)
COPY . .

# Copy entrypoint script (again) in case it was overwritten by COPY .
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose port
EXPOSE 8002

# Entrypoint command
CMD ["/wait-for-it.sh", "kafka:9092", "--", "./start.sh"]
