# Use the official Python 3.11 slim image as the base environment
FROM python:3.11-slim

# Update package lists and install essential system dependencies
# build-essential: Required for compiling certain Python packages
# libpq-dev: Required for PostgreSQL database connections (asyncpg)
# Clean up apt lists to reduce the image size
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies specified in requirements.txt
# --no-cache-dir is used to save space by not caching packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container
COPY . /app

# Expose port 8000 to allow external access to the API
EXPOSE 8000

# Command to run the application using Uvicorn
# app.main:app refers to the FastAPI instance in app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]