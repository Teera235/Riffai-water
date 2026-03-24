@echo off
REM Test Backend API

echo ========================================
echo Testing RIFFAI Backend API
echo ========================================
echo.

echo Testing health endpoint...
curl -s http://localhost:8000/health
echo.
echo.

echo Testing root endpoint...
curl -s http://localhost:8000/
echo.
echo.

echo Testing map/rivers endpoint...
curl -s http://localhost:8000/api/map/rivers
echo.
echo.

echo Testing map/dams endpoint...
curl -s http://localhost:8000/api/map/dams
echo.
echo.

echo Testing map/basins endpoint...
curl -s http://localhost:8000/api/map/basins
echo.
echo.

echo ========================================
echo Test Complete!
echo ========================================
echo.
echo If you see JSON responses above, the backend is working!
echo If you see errors, make sure backend is running:
echo   cd backend
echo   py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.

pause
