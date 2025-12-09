#!/bin/bash
clear

cat << "EOF"
   ___          _         ___                 ___      _                        
  | __|__ _ _ _| |_  _   / __|__ _ _ _ ___   / __|__ _| |_ _____ __ ____ _ _  _ 
  | _|/ _` | '_| | || | | (__/ _` | '_/ -_) | (_ / _` |  _/ -_) V  V / _` | || |
  |___\__,_|_| |_|\_, |  \___\__,_|_| \___|  \___\__,_|\__\___|\_/\_/\__,_|\_, |
                  |__/                                                     |__/ 
EOF

echo
echo "Building and starting Docker containers..."

docker-compose up --build

read -p "Press ENTER to exit..."