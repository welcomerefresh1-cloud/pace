#!/bin/bash

# PACE Development - Start Backend Server
# This script starts the FastAPI backend server with hot reload

echo "🚀 Starting PACE Backend Server..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/../backend" || exit 1

# Check if Redis is running
echo "⏳ Checking Redis connection..."
redis-cli ping > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Redis is running"
else
    echo "⚠️  Warning: Redis is not running. Use ./start-docker.sh to start it."
    echo ""
fi

# Check if Python venv exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/pydepcheck" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    touch .venv/pydepcheck
fi

echo ""
echo "✅ Environment ready. Starting FastAPI server..."
echo "📍 Backend will be available at: http://localhost:8000"
echo "📚 API Docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
