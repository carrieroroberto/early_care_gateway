# Use the official Python 3.11 slim image as the base
FROM python:3.11-slim

# Update package lists and install essential system dependencies
# build-essential: Compilers for Python extensions
# libpq-dev: PostgreSQL database adapter dependencies
# libgl1, libglib2.0-0: Required libraries for image processing (e.g., OpenCV, scikit-image)
# Clean up apt lists to keep image size small
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies specified in requirements.txt
# --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code into the container
COPY . /app

# Expose port 8000 for the API
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]