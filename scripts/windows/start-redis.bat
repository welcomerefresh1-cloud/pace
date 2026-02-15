@echo off
REM PACE Development - Start Redis Service (Windows)
REM This script starts Redis using Docker Compose

echo.
echo 🚀 Starting Redis Service...
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

echo ⏳ Starting Redis container...
docker-compose up -d redis

if errorlevel 1 (
    echo ❌ Failed to start Redis
    pause
    exit /b 1
)

echo.
echo ✅ Redis started successfully
echo.
echo 📋 Redis connection string:
echo    redis://localhost:6379
echo.
echo 🔍 View logs:
echo    docker-compose logs -f redis
echo.
echo ❌ To stop Redis:
echo    scripts\stop-redis.bat
echo.

pause
