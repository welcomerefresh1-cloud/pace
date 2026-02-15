@echo off
REM PACE Development - Start Backend Server (Windows)
REM This script starts the FastAPI backend server with hot reload

echo.
echo 🚀 Starting PACE Backend Server...
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%..\..\backend

REM Navigate to backend directory
cd /d "%BACKEND_DIR%" || exit /b 1

REM Check if Python venv exists
if not exist ".venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist ".venv\pydepcheck" (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    (
        echo. > .venv\pydepcheck
    )
)

echo.
echo ✅ Environment ready. Starting FastAPI server...
echo 📍 Backend will be available at: http://localhost:8000
echo 📚 API Docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
