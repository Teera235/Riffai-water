@echo off
REM Setup and run backend with Earth Engine

echo ========================================
echo RiffAI Backend Setup
echo ========================================
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Earth Engine Authentication
echo ========================================
echo.
echo Checking Earth Engine authentication...

python -c "import ee; ee.Initialize(); print('✅ Already authenticated')" 2>nul

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️  Earth Engine not authenticated
    echo.
    echo To authenticate, run:
    echo   python -m ee authenticate
    echo.
    echo Or continue without Earth Engine (will use mock data)
    echo.
    choice /C YN /M "Authenticate now"
    
    if errorlevel 2 (
        echo Continuing with mock data...
    ) else (
        python -m ee authenticate
    )
)

echo.
echo ========================================
echo Starting Backend Server
echo ========================================
echo.
echo Server will start on: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Test Earth Engine: http://127.0.0.1:8000/api/pipeline/test-ee
echo.
echo Press CTRL+C to stop
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
