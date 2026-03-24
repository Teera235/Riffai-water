@echo off
REM Upgrade Cloud Run Resources for Better Performance

echo ========================================
echo RIFFAI Platform - Resource Upgrade
echo ========================================
echo.
echo This will upgrade:
echo   Backend:  2 vCPU / 4 GiB (from 2 vCPU / 2 GiB)
echo   Frontend: 2 vCPU / 1 GiB (from 1 vCPU / 1 GiB)
echo.
echo Estimated cost: ~2,000 THB/month (~$57/month)
echo.
echo Benefits:
echo   - 2-3x faster response time
echo   - Better AI/ML performance
echo   - Faster cold starts
echo   - Higher concurrency
echo.
pause

echo.
echo ========================================
echo 1/2 Upgrading Backend...
echo ========================================
echo.

gcloud run services update riffai-backend ^
  --region asia-southeast1 ^
  --memory 4Gi ^
  --cpu 2 ^
  --max-instances 3 ^
  --concurrency 80 ^
  --timeout 300

if %errorlevel% neq 0 (
    echo ❌ Backend upgrade failed!
    pause
    exit /b 1
)

echo.
echo ✅ Backend upgraded successfully!
echo.

echo ========================================
echo 2/2 Upgrading Frontend...
echo ========================================
echo.

gcloud run services update riffai-frontend ^
  --region asia-southeast1 ^
  --memory 1Gi ^
  --cpu 2 ^
  --max-instances 3 ^
  --concurrency 100 ^
  --timeout 60

if %errorlevel% neq 0 (
    echo ❌ Frontend upgrade failed!
    pause
    exit /b 1
)

echo.
echo ✅ Frontend upgraded successfully!
echo.

echo ========================================
echo 🎉 Upgrade Complete!
echo ========================================
echo.
echo New Configuration:
echo.
echo Backend:
echo   - CPU: 2 vCPU
echo   - Memory: 4 GiB
echo   - Max instances: 3
echo   - Concurrency: 80
echo.
echo Frontend:
echo   - CPU: 2 vCPU
echo   - Memory: 1 GiB
echo   - Max instances: 3
echo   - Concurrency: 100
echo.
echo Your platform should be 2-3x faster now! 🚀
echo.
echo Test it:
echo   Backend:  https://riffai-backend-715107904640.asia-southeast1.run.app
echo   Frontend: https://riffai-frontend-715107904640.asia-southeast1.run.app
echo.
echo Monitor costs:
echo   https://console.cloud.google.com/billing
echo.

pause
