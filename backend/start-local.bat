@echo off
REM Start RiffAI Backend Locally with Virtual Environment

echo ========================================
echo RiffAI Backend - Local Development
echo ========================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo Starting Backend Server
echo ========================================
echo.
echo 🌐 Server: http://127.0.0.1:8000
echo 📚 API Docs: http://127.0.0.1:8000/docs
echo 🛰️  Test Earth Engine: http://127.0.0.1:8000/api/pipeline/test-ee
echo.
echo ⚠️  Earth Engine Status: Mock Mode (no authentication)
echo    To enable real data: python -m ee authenticate
echo.
echo Press CTRL+C to stop
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
