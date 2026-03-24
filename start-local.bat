@echo off
REM Start RIFFAI Platform Locally

echo ========================================
echo RIFFAI Platform - Local Development
echo ========================================
echo.

REM Check if ports are in use
echo Checking ports...
netstat -ano | findstr :8000 | findstr LISTENING >nul
if %errorlevel% equ 0 (
    echo ⚠️  Port 8000 is already in use!
    echo Run kill-ports.bat to free the port
    pause
    exit /b 1
)

netstat -ano | findstr :3000 | findstr LISTENING >nul
if %errorlevel% equ 0 (
    echo ⚠️  Port 3000 is already in use!
    echo Run kill-ports.bat to free the port
    pause
    exit /b 1
)

echo ✅ Ports are available
echo.
echo Starting services:
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:3000
echo   - API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C in each window to stop services
echo ========================================
echo.

REM Start Backend in new window
echo Starting Backend...
start "RIFFAI Backend" cmd /k "cd backend && py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 5 /nobreak

REM Start Frontend in new window
echo Starting Frontend...
start "RIFFAI Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo ✅ Services Started!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop services
echo ========================================
echo.

pause
