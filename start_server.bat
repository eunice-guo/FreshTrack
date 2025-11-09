@echo off
REM FreshTrack Backend Server Startup Script
REM This script starts the FastAPI backend server

echo ====================================
echo   FreshTrack Backend Server
echo ====================================
echo.

cd /d %~dp0backend

REM Check if data directory exists
if not exist "data" (
    echo Creating data directory...
    mkdir data
    echo.
)

REM Check if database exists
if not exist "data\freshtrack.db" (
    echo Database not found. Initializing with sample data...
    python init_sample_data.py
    echo.
)

echo Starting FreshTrack API server on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python main.py

pause
