@echo off
REM Seed production database on Cloud Run
echo ========================================
echo Seeding Production Database
echo ========================================
echo.

set PROJECT_ID=trim-descent-452802-t2
set REGION=asia-southeast1
set SERVICE=riffai-backend

echo Running seed script on Cloud Run...
gcloud run jobs create riffai-seed ^
  --image=asia-southeast1-docker.pkg.dev/%PROJECT_ID%/riffai/backend:latest ^
  --region=%REGION% ^
  --project=%PROJECT_ID% ^
  --set-env-vars="DATABASE_URL=postgresql+asyncpg://riffai:riffai123@/riffai?host=/cloudsql/%PROJECT_ID%:asia-southeast1:riffai-db" ^
  --set-cloudsql-instances=%PROJECT_ID%:asia-southeast1:riffai-db ^
  --command=python ^
  --args=-m,app.seed ^
  --max-retries=0 ^
  --task-timeout=600

echo.
echo Executing job...
gcloud run jobs execute riffai-seed ^
  --region=%REGION% ^
  --project=%PROJECT_ID% ^
  --wait

echo.
echo ========================================
echo Seed completed!
echo ========================================
