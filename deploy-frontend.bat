@echo off
REM Deploy RIFFAI Frontend to Cloud Run

echo ========================================
echo RIFFAI Frontend Deployment
echo ========================================
echo.

set PROJECT_ID=trim-descent-452802-t2
set REGION=asia-southeast1
set SERVICE_NAME=riffai-frontend
set BACKEND_URL=https://riffai-backend-715107904640.asia-southeast1.run.app

echo Project: %PROJECT_ID%
echo Region: %REGION%
echo Service: %SERVICE_NAME%
echo Backend: %BACKEND_URL%
echo.

echo ========================================
echo Step 1: Set Project
echo ========================================
echo.

gcloud config set project %PROJECT_ID%

echo.
echo ========================================
echo Step 2: Deploy to Cloud Run
echo ========================================
echo.

cd frontend

gcloud run deploy %SERVICE_NAME% ^
    --source . ^
    --region=%REGION% ^
    --platform=managed ^
    --allow-unauthenticated ^
    --memory=1Gi ^
    --cpu=1 ^
    --timeout=300 ^
    --set-env-vars="NEXT_PUBLIC_API_URL=%BACKEND_URL%" ^
    --build-env-vars="NEXT_PUBLIC_API_URL=%BACKEND_URL%"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ Deployment Successful!
    echo ========================================
    echo.
    echo Frontend is now live!
    echo.
    echo Get the URL:
    echo   gcloud run services describe %SERVICE_NAME% --region=%REGION% --format="value(status.url)"
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ Deployment Failed
    echo ========================================
    echo.
    echo Check the logs:
    echo   gcloud builds list --limit=1 --region=%REGION%
    echo.
)

cd ..
pause
