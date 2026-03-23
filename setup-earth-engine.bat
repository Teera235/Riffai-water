@echo off
REM Setup Google Earth Engine Authentication
REM สำหรับ Local Development

echo ========================================
echo Google Earth Engine Authentication
echo ========================================
echo.

REM Check if earthengine-api is installed
echo Checking earthengine-api installation...
pip show earthengine-api >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing earthengine-api...
    pip install earthengine-api geemap
    echo.
)

echo ========================================
echo Step 1: Authenticate Earth Engine
echo ========================================
echo.
echo This will open a browser for authentication.
echo Please sign in with your Google account.
echo.
pause

earthengine authenticate

echo.
echo ========================================
echo Step 2: Test Connection
echo ========================================
echo.

python -c "import ee; ee.Initialize(); print('✅ Earth Engine authenticated successfully!')"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ SUCCESS!
    echo ========================================
    echo.
    echo Earth Engine is now authenticated.
    echo You can now use real satellite data.
    echo.
    echo Next steps:
    echo   1. Run backend: cd backend ^&^& start-local.bat
    echo   2. Test API: http://localhost:8000/api/pipeline/test-ee
    echo   3. Fetch real data: POST /api/pipeline/fetch-satellite
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ Authentication Failed
    echo ========================================
    echo.
    echo Please try again or check:
    echo   - Internet connection
    echo   - Google account access
    echo   - Earth Engine access: https://earthengine.google.com/signup/
    echo.
)

pause
