FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0
ENV MONGO_URI=mongodb+srv://amrindersingh:7k9pHt7LcbOa8yqB@cluster0.6ememug.mongodb.net/
ENV MONGO_DB=hpe_inventory_test

# Create a non-root user
RUN useradd -m celeryuser
USER celeryuser

# Command to run the application
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"] 