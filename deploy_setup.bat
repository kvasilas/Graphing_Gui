@echo off
REM Deployment Setup Script for Graph Generator (Windows)
REM This script sets up a virtual environment and installs all dependencies

echo 🚀 Setting up Graph Generator virtual environment...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
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
echo ✅ Python %PYTHON_VERSION% detected

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ Failed to install dependencies. This might be due to:
    echo    - Network connectivity issues
    echo    - Python version compatibility
    echo    - Missing build tools
    echo.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

REM Verify installation
echo 🔍 Verifying installation...
python -c "import flask, numpy, pandas, plotly, werkzeug; print('✅ All packages installed successfully!'); print(f'Flask: {flask.__version__}'); print(f'NumPy: {numpy.__version__}'); print(f'Pandas: {pandas.__version__}'); print(f'Plotly: {plotly.__version__}'); print(f'Werkzeug: {werkzeug.__version__}')"

echo.
echo 🎉 Setup complete! 
echo.
echo 📋 Next steps:
echo    1. To activate the virtual environment:
echo       venv\Scripts\activate.bat
echo.
echo    2. To run the application:
echo       python app.py
echo.
echo    3. Open your browser and go to:
echo       http://localhost:5001
echo.
echo 💡 Tip: You can create a shortcut to run the app easily!
echo.
pause
