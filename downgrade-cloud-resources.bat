@echo off
REM Downgrade Cloud Run Resources to Save Cost

echo ========================================
echo RIFFAI Platform - Resource Downgrade
echo ========================================
echo.
echo This will downgrade back to:
echo   Backend:  2 vCPU / 2 GiB
echo   Frontend: 1 vCPU / 1 GiB
echo.
echo Estimated cost: ~730 THB/month (~$21/month)
echo.
echo ⚠️  Warning: Performance will be slower
echo.
pause

echo.
echo ========================================
echo 1/2 Downgrading Backend...
echo ========================================
echo.

gcloud run services update riffai-backend ^
  --region asia-southeast1 ^
  --memory 2Gi ^
  --cpu 2 ^
  --max-instances 10 ^
  --concurrency 80

if %errorlevel% neq 0 (
    echo ❌ Backend downgrade failed!
    pause
    exit /b 1
)

echo.
echo ✅ Backend downgraded
echo.

echo ========================================
echo 2/2 Downgrading Frontend...
echo ========================================
echo.

gcloud run services update riffai-frontend ^
  --region asia-southeast1 ^
  --memory 1Gi ^
  --cpu 1 ^
  --max-instances 10 ^
  --concurrency 80

if %errorlevel% neq 0 (
    echo ❌ Frontend downgrade failed!
    pause
    exit /b 1
)

echo.
echo ✅ Frontend downgraded
echo.

echo ========================================
echo Downgrade Complete
echo ========================================
echo.
echo Resources are back to original configuration
echo Cost: ~730 THB/month
echo.

pause
