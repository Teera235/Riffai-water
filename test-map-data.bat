@echo off
REM Test Map Data Endpoints

echo ========================================
echo Testing Map Data Endpoints
echo ========================================
echo.

echo 1. Testing Rivers...
echo.
curl -s http://localhost:8000/api/map/rivers | python -m json.tool
echo.
echo.

echo 2. Testing Dams...
echo.
curl -s http://localhost:8000/api/map/dams | python -m json.tool
echo.
echo.

echo 3. Testing Basins...
echo.
curl -s http://localhost:8000/api/map/basins | python -m json.tool
echo.
echo.

echo 4. Testing Stations...
echo.
curl -s http://localhost:8000/api/map/stations | python -m json.tool
echo.
echo.

echo 5. Testing Tiles Summary...
echo.
curl -s http://localhost:8000/api/map/tiles/summary | python -m json.tool
echo.
echo.

echo ========================================
echo Test Complete!
echo ========================================
echo.
echo If you see JSON data above, the backend is working correctly.
echo If you see errors, check:
echo   1. Backend is running (py -3 -m uvicorn app.main:app --reload --port 8000)
echo   2. Database has data (py -3 app/seed.py)
echo   3. No CORS errors
echo.

pause
