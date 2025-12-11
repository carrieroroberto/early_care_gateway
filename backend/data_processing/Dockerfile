# Use the official Python 3.11 slim image as the base environment
FROM python:3.11-slim

# Update package lists and install essential system dependencies
# build-essential: Required for compiling certain Python packages
# libpq-dev: Required for PostgreSQL database connections
# Clean up apt lists to keep the image size small
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip to the latest version to ensure smooth installation
RUN pip install --upgrade pip

# Install Python dependencies specified in requirements.txt
# --no-cache-dir is used to reduce the image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container
COPY . /app

# Expose port 8000 to allow traffic