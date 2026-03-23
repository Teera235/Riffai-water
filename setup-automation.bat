@echo off
REM Setup Cloud Scheduler jobs for automated data pipeline and model training

echo ========================================
echo Setting up Cloud Automation
echo ========================================
echo.

set PROJECT_ID=trim-descent-452802-t2
set REGION=asia-southeast1
set BACKEND_URL=https://riffai-backend-715107904640.asia-southeast1.run.app

echo Creating Cloud Scheduler jobs...
echo.

REM Job 1: Fetch water data every hour
echo [1/4] Creating hourly water data fetch job...
gcloud scheduler jobs create http fetch-water-hourly ^
  --location=%REGION% ^
  --schedule="0 * * * *" ^
  --uri="%BACKEND_URL%/api/pipeline/fetch-water" ^
  --http-method=POST ^
  --headers="Content-Type=application/json" ^
  --message-body="{}" ^
  --time-zone="Asia/Bangkok" ^
  --project=%PROJECT_ID%

echo.

REM Job 2: Fetch satellite data every 5 days
echo [2/4] Creating satellite data fetch job (every 5 days)...
gcloud scheduler jobs create http fetch-satellite-periodic ^
  --location=%REGION% ^
  --schedule="0 0 */5 * *" ^
  --uri="%BACKEND_URL%/api/pipeline/fetch-satellite" ^
  --http-method=POST ^
  --headers="Content-Type=application/json" ^
  --message-body="{}" ^
  --time-zone="Asia/Bangkok" ^
  --project=%PROJECT_ID%

echo.

REM Job 3: Check alerts every 30 minutes
echo [3/4] Creating alert check job (every 30 minutes)...
gcloud scheduler jobs create http check-alerts ^
  --location=%REGION% ^
  --schedule="*/30 * * * *" ^
  --uri="%BACKEND_URL%/api/alerts/check" ^
  --http-method=POST ^
  --headers="Content-Type=application/json" ^
  --message-body="{}" ^
  --time-zone="Asia/Bangkok" ^
  --project=%PROJECT_ID%

echo.

REM Job 4: Run predictions daily
echo [4/4] Creating daily prediction job...
gcloud scheduler jobs create http run-predictions-daily ^
  --location=%REGION% ^
  --schedule="0 6 * * *" ^
  --uri="%BACKEND_URL%/api/predict/batch" ^
  --http-method=POST ^
  --headers="Content-Type=application/json" ^
  --message-body="{\"basins\":[\"mekong_north\",\"eastern_coast\",\"southern_east\"],\"days_ahead\":30}" ^
  --time-zone="Asia/Bangkok" ^
  --project=%PROJECT_ID%

echo.
echo ========================================
echo Cloud Scheduler jobs created!
echo ========================================
echo.
echo Jobs:
echo   1. fetch-water-hourly      - Every hour
echo   2. fetch-satellite-periodic - Every 5 days
echo   3. check-alerts            - Every 30 minutes
echo   4. run-predictions-daily   - Daily at 6 AM
echo.
echo View jobs: https://console.cloud.google.com/cloudscheduler?project=%PROJECT_ID%
echo.
pause
