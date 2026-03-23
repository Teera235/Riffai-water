@echo off
REM Setup Earth Engine Service Account for Production
REM ใช้สำหรับ Cloud Run / Production deployment

echo ========================================
echo Earth Engine Service Account Setup
echo ========================================
echo.

set PROJECT_ID=trim-descent-452802-t2
set SERVICE_ACCOUNT_NAME=earth-engine-sa
set SERVICE_ACCOUNT_EMAIL=%SERVICE_ACCOUNT_NAME%@%PROJECT_ID%.iam.gserviceaccount.com
set KEY_FILE=earth-engine-key.json

echo Project: %PROJECT_ID%
echo Service Account: %SERVICE_ACCOUNT_EMAIL%
echo.

echo ========================================
echo Step 1: Create Service Account
echo ========================================
echo.

gcloud iam service-accounts create %SERVICE_ACCOUNT_NAME% ^
    --display-name="Earth Engine Service Account" ^
    --project=%PROJECT_ID%

if %errorlevel% neq 0 (
    echo Service account may already exist, continuing...
)

echo.
echo ========================================
echo Step 2: Grant Permissions
echo ========================================
echo.

REM Grant Earth Engine permissions
gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/earthengine.viewer"

gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/storage.objectViewer"

echo.
echo ========================================
echo Step 3: Create Key File
echo ========================================
echo.

gcloud iam service-accounts keys create %KEY_FILE% ^
    --iam-account=%SERVICE_ACCOUNT_EMAIL% ^
    --project=%PROJECT_ID%

if %errorlevel% equ 0 (
    echo.
    echo ✅ Key file created: %KEY_FILE%
    echo.
    
    echo ========================================
    echo Step 4: Register with Earth Engine
    echo ========================================
    echo.
    echo IMPORTANT: You need to register this service account with Earth Engine
    echo.
    echo 1. Go to: https://code.earthengine.google.com/
    echo 2. Sign in with your Google account
    echo 3. Click on "Assets" tab
    echo 4. Click "NEW" ^> "Cloud Project"
    echo 5. Enter project ID: %PROJECT_ID%
    echo 6. The service account will be automatically registered
    echo.
    echo OR use this command:
    echo.
    echo   earthengine set_project %PROJECT_ID%
    echo.
    pause
    
    echo.
    echo ========================================
    echo Step 5: Upload to Secret Manager
    echo ========================================
    echo.
    
    REM Create secret
    gcloud secrets create earth-engine-key ^
        --data-file=%KEY_FILE% ^
        --project=%PROJECT_ID% ^
        --replication-policy="automatic"
    
    if %errorlevel% neq 0 (
        echo Secret may already exist, updating...
        gcloud secrets versions add earth-engine-key ^
            --data-file=%KEY_FILE% ^
            --project=%PROJECT_ID%
    )
    
    echo.
    echo ========================================
    echo Step 6: Grant Cloud Run Access
    echo ========================================
    echo.
    
    REM Get Cloud Run service account
    for /f "tokens=*" %%i in ('gcloud run services describe riffai-backend --region=asia-southeast1 --project=%PROJECT_ID% --format="value(spec.template.spec.serviceAccountName)"') do set CLOUD_RUN_SA=%%i
    
    if "%CLOUD_RUN_SA%"=="" (
        set CLOUD_RUN_SA=%PROJECT_ID%@appspot.gserviceaccount.com
    )
    
    echo Cloud Run Service Account: %CLOUD_RUN_SA%
    echo.
    
    REM Grant secret access
    gcloud secrets add-iam-policy-binding earth-engine-key ^
        --member="serviceAccount:%CLOUD_RUN_SA%" ^
        --role="roles/secretmanager.secretAccessor" ^
        --project=%PROJECT_ID%
    
    echo.
    echo ========================================
    echo ✅ Setup Complete!
    echo ========================================
    echo.
    echo Service Account: %SERVICE_ACCOUNT_EMAIL%
    echo Key File: %KEY_FILE%
    echo Secret: earth-engine-key
    echo.
    echo Next steps:
    echo.
    echo 1. Update backend/.env:
    echo    GEE_SERVICE_ACCOUNT=%SERVICE_ACCOUNT_EMAIL%
    echo    GEE_KEY_FILE=%KEY_FILE%
    echo.
    echo 2. For Cloud Run, update cloudbuild.yaml to mount secret
    echo.
    echo 3. Redeploy backend:
    echo    cd backend
    echo    gcloud run deploy riffai-backend --source . --region=asia-southeast1
    echo.
    echo 4. Test:
    echo    curl https://riffai-backend-715107904640.asia-southeast1.run.app/api/pipeline/test-ee
    echo.
) else (
    echo.
    echo ❌ Failed to create key file
    echo.
)

pause
