#!/bin/bash

echo "========================================"
echo "  AI Interviewer - Quick Deploy Script"
echo "========================================"
echo ""

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.12+"
    exit 1
fi

python3 --version

echo ""
echo "Installing/Updating dependencies..."
python3 -m pip install --upgrade pip
pip3 install -r backend/requirements.txt

echo ""
echo "Setting up database..."
python3 -c "from backend.app.db import init_db; init_db()"

echo ""
echo "========================================"
echo "  Deployment Ready!"
echo "========================================"
echo ""
echo "Choose deployment option:"
echo ""
echo "1. Run locally (http://localhost:8000)"
echo "2. Run on network (accessible from other devices)"
echo "3. Build Docker image"
echo "4. Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Starting server on localhost:8000..."
        echo "Press Ctrl+C to stop"
        echo ""
        uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
        ;;
    2)
        echo ""
        echo "Finding your local IP address..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
        else
            # Linux
            IP=$(hostname -I | awk '{print $1}')
        fi
        echo ""
        echo "Starting server on network..."
        echo "Access from other devices at: http://$IP:8000"
        echo "Press Ctrl+C to stop"
        echo ""
        uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
        ;;
    3)
        echo ""
        echo "Building Docker image..."
        docker build -t ai-interviewer .
        echo ""
        echo "Docker image built successfully!"
        echo "Run with: docker-compose up -d"
        ;;
    4)
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
