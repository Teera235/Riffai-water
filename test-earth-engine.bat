@echo off
REM Test Earth Engine Integration

echo ========================================
echo Testing Earth Engine Integration
echo ========================================
echo.

cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Earth Engine...
pip install earthengine-api geemap --quiet

echo.
echo ========================================
echo Step 1: Authenticate Earth Engine
echo ========================================
echo.
echo This will open a browser for authentication.
echo Please login and authorize.
echo.
pause

earthengine authenticate

echo.
echo ========================================
echo Step 2: Test Connection
echo ========================================
echo.

python -c "import ee; ee.Initialize(); print('✅ Earth Engine connected successfully!')"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Step 3: Start Backend Server
    echo ========================================
    echo.
    echo Starting backend on http://localhost:8080
    echo.
    echo Test endpoints:
    echo   - http://localhost:8080/api/pipeline/test-ee
    echo   - http://localhost:8080/docs
    echo.
    echo Press Ctrl+C to stop
    echo.
    
    uvicorn app.main:app --reload
) else (
    echo.
    echo ❌ Earth Engine authentication failed
    echo Please run: earthengine authenticate
    echo.
    pause
)
