@echo off
REM Upload trained models to Cloud Storage

echo ========================================
echo Uploading AI Models to Cloud Storage
echo ========================================
echo.

set PROJECT_ID=trim-descent-452802-t2
set BUCKET_NAME=riffai-ai-models

REM Create bucket if not exists
echo Creating Cloud Storage bucket...
gsutil mb -p %PROJECT_ID% -l asia-southeast1 gs://%BUCKET_NAME% 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Bucket created
) else (
    echo ℹ️  Bucket already exists
)

echo.
echo Uploading models...
echo.

REM Upload models for each basin
for %%b in (mekong_north eastern_coast southern_east) do (
    echo [%%b] Uploading...
    
    if exist "ai-engine\models\trained\%%b\model.h5" (
        gsutil cp ai-engine\models\trained\%%b\model.h5 gs://%BUCKET_NAME%/%%b/model.h5
        gsutil cp ai-engine\models\trained\%%b\scalers.pkl gs://%BUCKET_NAME%/%%b/scalers.pkl
        gsutil cp ai-engine\models\trained\%%b\metrics.txt gs://%BUCKET_NAME%/%%b/metrics.txt
        echo   ✅ %%b uploaded
    ) else (
        echo   ⚠️  %%b model not found
    )
    echo.
)

echo ========================================
echo Upload Complete!
echo ========================================
echo.
echo View models: https://console.cloud.google.com/storage/browser/%BUCKET_NAME%?project=%PROJECT_ID%
echo.
pause
