@echo off
REM PACE Development - Docker Services Manager (Windows)
REM This script manages Redis and other Docker services using docker-compose

echo.
echo 🐳 PACE Docker Services Manager
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Navigate to project root
cd /d "%SCRIPT_DIR%..\.."

REM Check if docker is installed
where docker >nul 2>nul
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo.
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if docker-compose is available
where docker-compose >nul 2>nul
if errorlevel 1 (
    echo ❌ docker-compose is not available. Please ensure Docker Desktop is installed with docker-compose.
    pause
    exit /b 1
)

REM Parse command line arguments
if "%1"=="stop" (
    echo 🛑 Stopping Docker services...
    docker-compose down
    echo ✅ Docker services stopped
    pause
    exit /b 0
)

if "%1"=="restart" (
    echo 🔄 Restarting Docker services...
    docker-compose down
    docker-compose up -d
    echo ✅ Docker services restarted
    echo.
    echo 📍 Redis is running at: redis://localhost:6379
    pause
    exit /b 0
)

REM Default: start services
echo 🚀 Starting Docker services...
echo.

REM Check if services are already running
docker-compose ps 2>nul | find "Up" >nul
if not errorlevel 1 (
    echo ⚠️  Some services are already running.
    echo Use `start-docker.bat restart` to restart them.
    echo.
    docker-compose ps
) else (
    docker-compose up -d
    echo.
    echo ✅ Docker services started in background
    echo.
    echo 📍 Redis is running at: redis://localhost:6379
    echo.
    echo Available commands:
    echo   start-docker.bat stop     - Stop all services
    echo   start-docker.bat restart  - Restart all services
    echo.
    echo View logs with: docker-compose logs -f [service_name]
)

pause
