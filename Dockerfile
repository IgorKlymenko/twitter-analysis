# Use Python 3.12 slim as base image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /src

# Copy only the requirements file first to leverage Docker cache
COPY ./requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application source code
COPY . .

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "main.py"]
