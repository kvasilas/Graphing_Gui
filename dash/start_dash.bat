@echo off
REM Dash Graphing Tool Startup Script for Windows
REM This script sets up and runs the Dash version of the Graphing Tool

echo Starting Dash Graphing Tool Setup...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python detected

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
) else (
    echo Virtual environment found
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully

REM Check if app.py exists
if not exist "app.py" (
    echo app.py not found in current directory
    pause
    exit /b 1
)

echo Starting Dash Graphing Tool...
echo The application will be available at: http://localhost:8050
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the application
python app.py

pause
