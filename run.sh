#!/bin/bash
clear

cat << "EOF"
   ___          _         ___                 ___      _                        
  | __|__ _ _ _| |_  _   / __|__ _ _ _ ___   / __|__ _| |_ _____ __ ____ _ _  _ 
  | _|/ _` | '_| | || | | (__/ _` | '_/ -_) | (_ / _` |  _/ -_) V  V / _` | || |
  |___\__,_|_| |_|\_, |  \___\__,_|_| \___|  \___\__,_|\__\___|\_/\_/\__,_|\_, |
                  |__/                                                     |__/ 
EOF

echo "Starting containers..."
docker-compose up --build -d

echo
echo "Waiting for services to be ready..."

wait_http() {
    URL=$1
    NAME=$2

    echo "Waiting for $NAME service..."

    until curl -fs -o /dev/null "$URL"; do
        sleep 1
    done
}

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

pip install --upgrade pip
pip install -r tests/requirements.txt

echo
echo "Running tests..."
pytest tests

deactivate