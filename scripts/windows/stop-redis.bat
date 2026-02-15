@echo off
REM PACE Development - Stop Redis Service (Windows)
REM This script stops Redis using Docker Compose

echo.
echo 🛑 Stopping Redis Service...
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Navigate to project root
cd /d "%SCRIPT_DIR%..\.."

REM Check if docker-compose is available
where docker-compose >nul 2>nul
if errorlevel 1 (
    echo ❌ docker-compose is not installed.
    pause
    exit /b 1
)

REM Check if Redis container is running
docker-compose ps redis 2>nul | find "Up" >nul
if errorlevel 1 (
    echo ⚠️  Redis is not running.
    echo.
    pause
    exit /b 0
)

echo ⏳ Stopping Redis container...
docker-compose stop redis

if errorlevel 1 (
    echo ❌ Failed to stop Redis
    pause
    exit /b 1
)

echo.
echo ✅ Redis stopped successfully
echo.
echo 🚀 To start Redis again:
echo    scripts\start-redis.bat
echo.

pause
