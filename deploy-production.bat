@echo off
REM Deploy RIFFAI Platform to Production

echo ========================================
echo RIFFAI Platform - Production Deployment
echo ========================================
echo.
echo This will deploy to Google Cloud Run:
echo   Backend:  https://riffai-backend-715107904640.asia-southeast1.run.app
echo   Frontend: https://riffai-frontend-715107904640.asia-southeast1.run.app
echo.
echo Configuration:
echo   Backend:  2 vCPU / 4 GiB
echo   Frontend: 2 vCPU / 1 GiB
echo   Cost: ~2,000 THB/month
echo.
echo ⚠️  This will rebuild and redeploy everything!
echo.
pause

REM Check if logged in
echo.
echo Checking GCloud authentication...
gcloud auth list
if %errorlevel% neq 0 (
    echo ❌ Not logged in to GCloud!
    echo Please run: gcloud auth login
    pause
    exit /b 1
)

echo.
echo ========================================
echo 1/4 Building Backend Docker Image...
echo ========================================
cd backend
docker build -t gcr.io/trim-descent-452802-t2/riffai-backend:latest .
if %errorlevel% neq 0 (
    echo ❌ Backend build failed!
    cd ..
    pause
    exit /b 1
)
echo ✅ Backend image built
cd ..

echo.
echo ========================================
echo 2/4 Pushing Backend to GCR...
echo ========================================
docker push gcr.io/trim-descent-452802-t2/riffai-backend:latest
if %errorlevel% neq 0 (
    echo ❌ Backend push failed!
    pause
    exit /b 1
)
echo ✅ Backend image pushed

echo.
echo ========================================
echo 3/4 Deploying Backend to Cloud Run...
echo ========================================
gcloud run deploy riffai-backend ^
  --image gcr.io/trim-descent-452802-t2/riffai-backend:latest ^
  --platform managed ^
  --region asia-southeast1 ^
  --allow-unauthenticated ^
  --memory 4Gi ^
  --cpu 2 ^
  --max-instances 3 ^
  --concurrency 80 ^
  --timeout 300

if %errorlevel% neq 0 (
    echo ❌ Backend deployment failed!
    pause
    exit /b 1
)
echo ✅ Backend deployed

echo.
echo ========================================
echo 4/4 Building Frontend Docker Image...
echo ========================================
cd frontend
docker build -t gcr.io/trim-descent-452802-t2/riffai-frontend:latest .
if %errorlevel% neq 0 (
    echo ❌ Frontend build failed!
    cd ..
    pause
    exit /b 1
)
echo ✅ Frontend image built
cd ..

echo.
echo ========================================
echo 5/4 Pushing Frontend to GCR...
echo ========================================
docker push gcr.io/trim-descent-452802-t2/riffai-frontend:latest
if %errorlevel% neq 0 (
    echo ❌ Frontend push failed!
    pause
    exit /b 1
)
echo ✅ Frontend image pushed

echo.
echo ========================================
echo 6/4 Deploying Frontend to Cloud Run...
echo ========================================
gcloud run deploy riffai-frontend ^
  --image gcr.io/trim-descent-452802-t2/riffai-frontend:latest ^
  --platform managed ^
  --region asia-southeast1 ^
  --allow-unauthenticated ^
  --memory 1Gi ^
  --cpu 2 ^
  --max-instances 3 ^
  --concurrency 100 ^
  --timeout 60

if %errorlevel% neq 0 (
    echo ❌ Frontend deployment failed!
    pause
    exit /b 1
)
echo ✅ Frontend deployed

echo.
echo ========================================
echo 🎉 Production Deployment Complete!
echo ========================================
echo.
echo Your platform is now live at:
echo.
echo 🌐 Frontend:
echo https://riffai-frontend-715107904640.asia-southeast1.run.app
echo.
echo 🔌 Backend API:
echo https://riffai-backend-715107904640.asia-southeast1.run.app
echo.
echo 📚 API Documentation:
echo https://riffai-backend-715107904640.asia-southeast1.run.app/docs
echo.
echo ========================================
echo 🧪 Testing Deployment...
echo ========================================
echo.

echo Testing backend health...
curl -s https://riffai-backend-715107904640.asia-southeast1.run.app/health
echo.
echo.

echo Testing map endpoints...
curl -s https://riffai-backend-715107904640.asia-southeast1.run.app/api/map/rivers -o nul
if %errorlevel% equ 0 (
    echo ✅ Rivers endpoint OK
) else (
    echo ❌ Rivers endpoint failed
)

curl -s https://riffai-backend-715107904640.asia-southeast1.run.app/api/map/dams -o nul
if %errorlevel% equ 0 (
    echo ✅ Dams endpoint OK
) else (
    echo ❌ Dams endpoint failed
)

echo.
echo ========================================
echo 📊 Next Steps
echo ========================================
echo.
echo 1. Open frontend URL in browser
echo 2. Test all features
echo 3. Check map page displays data
echo 4. Monitor logs:
echo    gcloud run services logs read riffai-backend --region asia-southeast1
echo.
echo 5. Monitor costs:
echo    https://console.cloud.google.com/billing
echo.
echo 6. Set up monitoring alerts
echo 7. Configure custom domain (optional)
echo.

pause
