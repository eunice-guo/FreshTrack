#!/bin/bash
# FreshTrack Backend Server Startup Script
# This script starts the FastAPI backend server

echo "===================================="
echo "  FreshTrack Backend Server"
echo "===================================="
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "Creating data directory..."
    mkdir -p data
    echo ""
fi

# Check if database exists
if [ ! -f "data/freshtrack.db" ]; then
    echo "Database not found. Initializing with sample data..."
    python init_sample_data.py
    echo ""
fi

echo "Starting FreshTrack API server on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "===================================="
echo ""

python main.py
