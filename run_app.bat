@echo off
echo 🌍 EcoSolvE - Intelligent Solvent Prediction Platform
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo 📦 Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
    echo.
)

REM Create necessary directories
if not exist models mkdir models
if not exist data mkdir data
if not exist logs mkdir logs
if not exist exports mkdir exports
if not exist uploads mkdir uploads

echo 🚀 Starting EcoSolvE application...
echo 🌐 The application will be available at: http://localhost:8501
echo 📱 Press Ctrl+C to stop the application
echo.

REM Run the application
python -m streamlit run app.py --server.port 8501 --server.address localhost

pause
