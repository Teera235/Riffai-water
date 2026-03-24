@echo off
REM Kill processes using ports 8000 and 3000

echo ========================================
echo Killing processes on ports 8000 and 3000
echo ========================================
echo.

REM Kill port 8000 (Backend)
echo Checking port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process %%a on port 8000
    taskkill /F /PID %%a
)

REM Kill port 3000 (Frontend)
echo Checking port 3000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    echo Killing process %%a on port 3000
    taskkill /F /PID %%a
)

echo.
echo ========================================
echo Done! Ports 8000 and 3000 are now free
echo ========================================
echo.

pause
