@echo off
REM Fix Map Display Issues

echo ========================================
echo RIFFAI - Fix Map Display
echo ========================================
echo.
echo This script will:
echo   1. Check if backend is running
echo   2. Test API endpoints
echo   3. Restart frontend if needed
echo.
pause

echo.
echo Step 1: Checking Backend...
echo ========================================
curl -s http://localhost:8000/health
if %errorlevel% neq 0 (
    echo.
    echo ❌ Backend is NOT running!
    echo.
    echo Please start backend first:
    echo   cd backend
    echo   py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    echo.
    pause
    exit /b 1
)
echo.
echo ✅ Backend is running
echo.

echo Step 2: Testing Map Endpoints...
echo ========================================
echo.

echo Testing /api/map/rivers...
curl -s http://localhost:8000/api/map/rivers > nul
if %errorlevel% neq 0 (
    echo ❌ Rivers endpoint failed
) else (
    echo ✅ Rivers endpoint OK
)

echo Testing /api/map/dams...
curl -s http://localhost:8000/api/map/dams > nul
if %errorlevel% neq 0 (
    echo ❌ Dams endpoint failed
) else (
    echo ✅ Dams endpoint OK
)

echo Testing /api/map/basins...
curl -s http://localhost:8000/api/map/basins > nul
if %errorlevel% neq 0 (
    echo ❌ Basins endpoint failed
) else (
    echo ✅ Basins endpoint OK
)

echo Testing /api/map/tiles/summary...
curl -s http://localhost:8000/api/map/tiles/summary > nul
if %errorlevel% neq 0 (
    echo ❌ Tiles endpoint failed
) else (
    echo ✅ Tiles endpoint OK
)

echo.
echo Step 3: Checking Frontend...
echo ========================================
netstat -ano | findstr :3000 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo ⚠️  Frontend is NOT running
    echo.
    echo Please start frontend:
    echo   cd frontend
    echo   npm run dev
    echo.
) else (
    echo ✅ Frontend is running on port 3000
)

echo.
echo ========================================
echo Diagnosis Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Open browser: http://localhost:3000/map
echo   2. Open DevTools (F12)
echo   3. Check Console for errors
echo   4. Check Network tab for failed requests
echo.
echo If map still doesn't show data:
echo   - Clear browser cache (Ctrl+Shift+Delete)
echo   - Hard refresh (Ctrl+F5)
echo   - Check browser console for errors
echo.

pause
