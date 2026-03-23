@echo off
REM RIFFAI Platform - GCP Cloud Run Deployment Script (Windows)
REM ใช้สคริปต์นี้เพื่อ deploy ขึ้น Google Cloud Run

echo.
echo ========================================
echo   RIFFAI Platform - GCP Deployment
echo ========================================
echo.

REM ตรวจสอบ gcloud CLI
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] gcloud CLI ไม่ได้ติดตั้ง
    echo ติดตั้งที่: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM ตั้งค่า Project ID
set /p PROJECT_ID="GCP Project ID: "
if "%PROJECT_ID%"=="" (
    echo [ERROR] กรุณาใส่ Project ID
    pause
    exit /b 1
)

gcloud config set project %PROJECT_ID%
set REGION=asia-southeast1

echo.
echo [1/4] กำลัง Enable APIs...
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

echo.
echo [2/4] กำลัง Deploy Backend...
cd backend
gcloud run deploy riffai-backend --source . --region=%REGION% --platform=managed --allow-unauthenticated --memory=1Gi --cpu=1 --timeout=300

REM เก็บ Backend URL
for /f "tokens=*" %%i in ('gcloud run services describe riffai-backend --region=%REGION% --format="value(status.url)"') do set BACKEND_URL=%%i
echo Backend URL: %BACKEND_URL%

cd ..

echo.
echo [3/4] กำลัง Deploy Frontend...
cd frontend
gcloud run deploy riffai-frontend --source . --region=%REGION% --platform=managed --allow-unauthenticated --set-env-vars="NEXT_PUBLIC_API_URL=%BACKEND_URL%" --memory=512Mi --cpu=1

REM เก็บ Frontend URL
for /f "tokens=*" %%i in ('gcloud run services describe riffai-frontend --region=%REGION% --format="value(status.url)"') do set FRONTEND_URL=%%i

cd ..

echo.
echo ========================================
echo   Deployment สำเร็จ!
echo ========================================
echo.
echo Backend:  %BACKEND_URL%
echo Frontend: %FRONTEND_URL%
echo API Docs: %BACKEND_URL%/docs
echo.
echo [หมายเหตุ] ยังไม่ได้เชื่อม Cloud SQL
echo ตอนนี้ใช้ SQLite ชั่วคราว (ข้อมูลหายเมื่อ restart)
echo.
echo ถ้าต้องการใช้ Cloud SQL ดูคู่มือที่:
echo   DEPLOY-QUICK.md
echo   DEPLOYMENT-CHECKLIST.md
echo.
pause
