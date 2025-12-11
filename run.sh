#!/bin/bash
clear
# Clears the terminal window.

cat << "EOF"
   ___          _         ___                 ___      _                        
  | __|__ _ _ _| |_  _   / __|__ _ _ _ ___   / __|__ _| |_ _____ __ ____ _ _  _ 
  | _|/ _` | '_| | || | | (__/ _` | '_/ -_) | (_ / _` |  _/ -_) V  V / _` | || |
  |___\__,_|_| |_|\_, |  \___\__,_|_| \___|  \___\__,_|\__\___|\_/\_/\__,_|\_, |
                  |__/                                                     |__/ 
EOF
# Prints ASCII art using a here-document. Quoted "EOF" prevents variable expansion.

echo "Starting containers..."
docker-compose up --build -d
# Builds and starts Docker containers in detached mode.

echo
echo "Waiting for services to be ready..."

# Function that waits until an HTTP endpoint becomes available.
wait_http() {
    URL=$1     # Endpoint to check
    NAME=$2    # Human-readable service name

    echo "Waiting for $NAME service..."

    # Loop until curl returns success (-f ensures failure on HTTP errors)
    until curl -fs -o /dev/null "$URL"; do
        sleep 1   # Wait 1 second before retrying
    done
}

# Check readiness of each microservice's /docs endpoint
wait_http http://localhost:8001/docs "AUDIT"
wait_http http://localhost:8000/docs "AUTH"
wait_http http://localhost:8004/docs "DATA"
wait_http http://localhost:8003/docs "XAI"
wait_http http://localhost:8002/docs "GATEWAY"

echo
echo "All services are ready."

echo "Installing Python test dependencies..."
python3 -m venv venv
source venv/bin/activate
# Creates and activates a Python virtual environment.

pip install --upgrade pip
pip install -r tests/requirements.txt
# Installs required packages for testing.

echo
echo "Running tests..."
pytest tests
# Runs all tests inside the 'tests' directory.

deactivate
# Deactivates the virtual environment.
