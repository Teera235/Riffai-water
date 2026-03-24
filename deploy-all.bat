@echo off
REM Deploy entire RIFFAI Platform to Google Cloud

echo ========================================
echo RIFFAI Platform - Full Deployment
echo ========================================
echo.
echo This will deploy:
echo   1. Backend API (FastAPI)
echo   2. Frontend (Next.js)
echo.
echo Project: trim-descent-452802-t2
echo Region: asia-southeast1
echo.
pause

REM Deploy Backend
echo.
echo ========================================
echo 1/2 Deploying Backend...
echo ========================================
cd backend
call deploy-backend.bat
if %errorlevel% neq 0 (
    echo ❌ Backend deployment failed!
    cd ..
    exit /b 1
)
cd ..

REM Wait a bit for backend to be ready
echo.
echo ⏳ Waiting for backend to be ready...
timeout /t 10 /nobreak

REM Deploy Frontend
echo.
echo ========================================
echo 2/2 Deploying Frontend...
echo ========================================
cd frontend
call deploy-frontend.bat
if %errorlevel% neq 0 (
    echo ❌ Frontend deployment failed!
    cd ..
    exit /b 1
)
cd ..

REM Summary
echo.
echo ========================================
echo 🎉 Full Deployment Complete!
echo ========================================
echo.
echo ✅ Backend deployed
echo ✅ Frontend deployed
echo.
echo 🌐 Access your platform:
echo.
echo Backend API:
gcloud run services describe riffai-backend --region asia-southeast1 --format "value(status.url)"
echo.
echo Frontend:
gcloud run services describe riffai-frontend --region asia-southeast1 --format "value(status.url)"
echo.
echo 📚 API Documentation:
gcloud run services describe riffai-backend --region asia-southeast1 --format "value(status.url)"
echo /docs
echo.
echo ========================================
echo 🚀 RIFFAI Platform is Live!
echo ========================================
echo.

pause
