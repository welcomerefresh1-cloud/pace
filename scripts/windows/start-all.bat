@echo off
REM PACE Development - Start All Services (Windows)
REM This script provides easy startup of all development services

echo.
echo 🚀 PACE Development - Start All Services
echo.

REM Get the directory where this script is located and navigate to project root
set SCRIPT_DIR="%~dp0"
cd /d "%SCRIPT_DIR%..\.."

echo Checking prerequisites...
echo.

REM Check Docker
where docker >nul 2>nul
if errorlevel 1 (
    echo ❌ Docker not found
    set DOCKER_OK=0
) else (
    echo ✅ Docker found
    set DOCKER_OK=1
)

REM Check Node
where node >nul 2>nul
if errorlevel 1 (
    echo ❌ Node.js not found
    set NODE_OK=0
) else (
    echo ✅ Node.js found
    set NODE_OK=1
)

REM Check Python
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python not found
    set PYTHON_OK=0
) else (
    echo ✅ Python found
    set PYTHON_OK=1
)

echo.

REM Try to start services in new command prompts
echo 🔧 Starting services in separate windows...
echo.

REM Start Docker in new window
start "PACE - Docker" call scripts\start-docker.bat

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start Backend in new window
start "PACE - Backend" call scripts\start-backend.bat

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start Frontend in new window
start "PACE - Frontend" call scripts\start-frontend.bat

echo ✅ All services started in separate windows
echo.
echo 📍 Once services are running:
echo    Backend API:    http://localhost:8000
echo    API Docs:       http://localhost:8000/docs
echo    Frontend:       http://localhost:3000
echo.
echo 📋 You should see three new command prompt windows:
echo    1. Docker Services (Redis, Database)
echo    2. Backend (FastAPI on port 8000)
echo    3. Frontend (Next.js on port 3000)
echo.
echo Close each window individually to stop specific services.
echo.

pause
