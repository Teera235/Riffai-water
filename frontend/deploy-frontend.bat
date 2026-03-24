@echo off
REM Deploy RIFFAI Frontend to Google Cloud Run

echo ========================================
echo RIFFAI Frontend - Cloud Run Deployment
echo ========================================
echo.

REM Configuration
set PROJECT_ID=trim-descent-452802-t2
set REGION=asia-southeast1
set SERVICE_NAME=riffai-frontend
set IMAGE_NAME=gcr.io/%PROJECT_ID%/%SERVICE_NAME%
set BACKEND_URL=https://riffai-backend-715107904640.asia-southeast1.run.app

echo 📦 Project: %PROJECT_ID%
echo 🌏 Region: %REGION%
echo 🚀 Service: %SERVICE_NAME%
echo 🔗 Backend: %BACKEND_URL%
echo.

REM Set project
echo Setting GCP project...
gcloud config set project %PROJECT_ID%
echo.

REM Build Docker image
echo 🔨 Building Docker image...
docker build -t %IMAGE_NAME% .
if %errorlevel% neq 0 (
    echo ❌ Docker build failed!
    exit /b 1
)
echo ✅ Docker image built successfully
echo.

REM Push to Google Container Registry
echo 📤 Pushing image to GCR...
docker push %IMAGE_NAME%
if %errorlevel% neq 0 (
    echo ❌ Docker push failed!
    exit /b 1
)
echo ✅ Image pushed successfully
echo.

REM Deploy to Cloud Run
echo 🚀 Deploying to Cloud Run...
gcloud run deploy %SERVICE_NAME% ^
    --image %IMAGE_NAME% ^
    --platform managed ^
    --region %REGION% ^
    --allow-unauthenticated ^
    --memory 1Gi ^
    --cpu 1 ^
    --timeout 300 ^
    --max-instances 10 ^
    --set-env-vars "NEXT_PUBLIC_API_URL=%BACKEND_URL%"

if %errorlevel% neq 0 (
    echo ❌ Deployment failed!
    exit /b 1
)

echo.
echo ========================================
echo ✅ Deployment Successful!
echo ========================================
echo.
echo 🌐 Frontend URL:
gcloud run services describe %SERVICE_NAME% --region %REGION% --format "value(status.url)"
echo.
echo 🎉 RIFFAI Platform is now live!
echo.

pause
