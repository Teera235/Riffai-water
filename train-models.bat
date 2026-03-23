@echo off
REM Train AI models using data from Cloud SQL

echo ========================================
echo Training HydroLSTM Models
echo ========================================
echo.

cd ai-engine

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install asyncpg psycopg2-binary sqlalchemy

echo.
echo ========================================
echo Starting Training
echo ========================================
echo.

REM Set database URL
set DATABASE_URL=postgresql+asyncpg://riffai:riffai123@34.21.160.173/riffai

REM Train all basins
python training\train_model.py --basin all --epochs 50 --batch-size 32

echo.
echo ========================================
echo Training Complete!
echo ========================================
echo.
echo Models saved to: ai-engine\models\trained\
echo.
pause
