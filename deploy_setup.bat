@echo off
REM Deployment Setup Script for Graph Generator (Windows)
REM This script sets up a virtual environment and installs all dependencies

echo Setting up Graph Generator virtual environment...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    echo After installing Python, close and reopen this window, then try again.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo SUCCESS: Python %PYTHON_VERSION% detected

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

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
    echo.
    echo ERROR: Failed to install dependencies. This might be due to:
    echo    - Network connectivity issues
    echo    - Python version compatibility
    echo    - Missing build tools
    echo.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

REM Verify installation
echo Verifying installation...
python -c "import flask, numpy, pandas, plotly, werkzeug; print('SUCCESS: All packages installed successfully!'); print(f'Flask: {flask.__version__}'); print(f'NumPy: {numpy.__version__}'); print(f'Pandas: {pandas.__version__}'); print(f'Plotly: {plotly.__version__}'); print(f'Werkzeug: {werkzeug.__version__}')"

echo.
echo If app doesnt open click the link below
echo Access at: http://localhost:5001
echo.

REM Start the application
echo Starting Graph Generator application...
echo Press Ctrl+C to stop the application
echo.

REM Start the app and handle cleanup
python app.py

REM Cleanup when app exits
echo.
echo Cleaning up...
REM Kill any remaining Python processes on port 5001
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5001 2^>nul') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo Application stopped.
pause