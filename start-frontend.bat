@echo off
REM Start Frontend Locally

echo ========================================
echo RIFFAI Frontend - Local Development
echo ========================================
echo.

cd frontend

echo Installing dependencies...
call npm install

echo.
echo ========================================
echo Starting Frontend
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🗺️  Map: http://localhost:3000/map
echo 🤖 Predict: http://localhost:3000/predict
echo.
echo Press CTRL+C to stop
echo.

npm run dev
