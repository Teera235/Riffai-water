@echo off
echo ========================================
echo Starting RiffAI Backend Server
echo ========================================
echo.
echo Server: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Press CTRL+C to stop
echo.

py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
