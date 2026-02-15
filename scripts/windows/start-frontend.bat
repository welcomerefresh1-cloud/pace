@echo off
REM PACE Development - Start Frontend Server (Windows)
REM This script starts the Next.js frontend development server

echo.
echo 🚀 Starting PACE Frontend Server...
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Navigate to project root
cd /d "%SCRIPT_DIR%..\.."

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    call npm install
)

echo.
echo ✅ Dependencies ready. Starting Next.js dev server...
echo 📍 Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the development server
call npm run dev

pause
