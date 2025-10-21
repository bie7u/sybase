# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies for pymssql
RUN apt-get update && apt-get install -y \
    freetds-dev \
    freetds-bin \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py .
COPY .env.example .

# Expose port
EXPOSE 8000

# Set environment variables (override with docker run -e)
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Run the application
CMD ["python", "main.py"]
