@echo off
REM Start RIFFAI Platform with Docker Compose

echo ========================================
echo RIFFAI Platform - Docker Compose
echo ========================================
echo.

echo 🐳 Starting containers...
docker-compose up -d

if %errorlevel% neq 0 (
    echo ❌ Failed to start containers!
    exit /b 1
)

echo.
echo ✅ Containers started successfully!
echo.
echo 🌐 Services:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo.
echo 📊 View logs:
echo   docker-compose logs -f
echo.
echo 🛑 Stop containers:
echo   docker-compose down
echo.

pause
