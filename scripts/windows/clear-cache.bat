@echo off
REM PACE Development - Clear Redis Cache (Windows)
REM This script clears all cached data from Redis

echo.
echo 🗑️  PACE Cache Clear Tool
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

REM Check if Redis is running
docker-compose ps redis 2>nul | find "Up" >nul
if errorlevel 1 (
    echo ⚠️  Redis is not running. Starting Redis...
    docker-compose up -d redis
    timeout /t 2 /nobreak >nul
)

echo Are you sure you want to clear ALL cache? This is irreversible. (y/N)
set /p confirm=

if /i not "%confirm%"=="y" (
    echo ❌ Cache clear cancelled.
    echo.
    pause
    exit /b 0
)

echo.
echo ⏳ Clearing cache...

REM Get count before
for /f "tokens=*" %%A in ('docker-compose exec -T redis redis-cli DBSIZE 2^>nul') do (
    set "output=%%A"
)
echo 📊 Redis DBSIZE: %output%

REM Clear the database
docker-compose exec -T redis redis-cli FLUSHDB >nul 2>&1

if errorlevel 1 (
    echo ❌ Failed to clear cache
    pause
    exit /b 1
)

echo.
echo ✅ Cache cleared successfully!
echo.
echo 📊 Keys after clear: 0
echo.
echo 💡 Next steps:
echo    - Restart the backend to reload cache on startup
echo    - Or let the cache auto-refresh (jobs refresh every 6 hours)
echo.

pause
