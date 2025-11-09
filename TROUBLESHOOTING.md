# FreshTrack Troubleshooting Guide

## Issue: Receipt Upload Failed - ERR_CONNECTION_REFUSED

### Problem Description
When trying to upload and scan a receipt via the web interface, you encounter:
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
localhost:8000/api/receipt/upload/1:1 Failed to load resource: net::ERR_CONNECTION_REFUSED
Upload error: TypeError: Failed to fetch
```

### Root Cause
The web interface (located in `web/index.html`) requires the backend API server to be running on `http://localhost:8000`. The error `ERR_CONNECTION_REFUSED` indicates that:

1. **The backend server is NOT running** - The FastAPI server needs to be started
2. The web interface cannot communicate with the API endpoints

### Solution

Follow these steps to fix the issue:

#### Step 1: Start the Backend Server

```bash
# Navigate to the backend directory
cd backend

# Create the data directory if it doesn't exist
mkdir -p data

# Initialize the database with sample data (first time only)
python init_sample_data.py

# Start the FastAPI server
python main.py
```

You should see output like:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
✅ Database initialized!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### Step 2: Open the Web Interface

**Option A: Using Python HTTP Server (Recommended for Windows)**
```bash
# In a NEW terminal/command prompt, navigate to the web directory
cd web

# Start a simple HTTP server
python -m http.server 3000
```

Then open your browser to: `http://localhost:3000`

**Option B: Direct File Access (May have CORS issues)**
```bash
# Open the HTML file directly
cd web
start index.html  # Windows
# OR
open index.html   # macOS
# OR
xdg-open index.html  # Linux
```

Then the web interface should work at: `file:///path/to/FreshTrack/web/index.html`

#### Step 3: Verify Connection

1. Open your browser's Developer Tools (F12)
2. Check the Console tab - you should no longer see connection errors
3. Try uploading a receipt image

### Verification Checklist

- [ ] Backend server is running on port 8000
- [ ] You can access the API docs at `http://localhost:8000/docs`
- [ ] Web interface can load data from the dashboard
- [ ] No `ERR_CONNECTION_REFUSED` errors in browser console

### Common Issues

#### Port 8000 Already in Use
If you see an error like `Address already in use`, another application is using port 8000.

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

#### Database Not Initialized
If you get database errors, reinitialize the database:
```bash
cd backend
rm -rf data/freshtrack.db  # Remove old database
python init_sample_data.py  # Recreate with sample data
```

#### Missing Dependencies
If you get `ModuleNotFoundError`, install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

#### Tesseract OCR Not Found
The receipt scanning feature requires Tesseract OCR. Install it:

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location
3. Add to PATH: `C:\Program Files\Tesseract-OCR`

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

### Architecture Overview

```
┌─────────────────┐         HTTP Requests         ┌──────────────────┐
│  Web Interface  │ ──────────────────────────────>│  Backend Server  │
│  (index.html)   │    localhost:8000/api/*        │   (main.py)      │
│                 │ <──────────────────────────────│   Port: 8000     │
└─────────────────┘         JSON Responses         └──────────────────┘
                                                            │
                                                            │ SQLite
                                                            ▼
                                                    ┌──────────────┐
                                                    │   Database   │
                                                    │ freshtrack.db│
                                                    └──────────────┘
```

### File Locations

- **Web Interface**: `/web/index.html`, `/web/app.js`, `/web/styles.css`
- **Backend Server**: `/backend/main.py`
- **Database**: `/backend/data/freshtrack.db`
- **API Configuration**: `/backend/main.py` (line 2: `API_BASE_URL = 'http://localhost:8000'`)

### Testing the API Directly

You can test if the backend is working by visiting these URLs in your browser:

1. Health check: `http://localhost:8000/`
2. API docs: `http://localhost:8000/docs`
3. Get user stats: `http://localhost:8000/api/stats/1`
4. Get food items: `http://localhost:8000/api/items/1`

### Need More Help?

1. Check the [README.md](README.md) for full setup instructions
2. Review the [API documentation](http://localhost:8000/docs) (when server is running)
3. Check server logs in the terminal where you ran `python main.py`
4. Look for error messages in the browser's Developer Tools Console

---

**Last Updated**: 2025-11-09
