#!/bin/bash

# Dash Graphing Tool Startup Script
# This script sets up and runs the Dash version of the Graphing Tool

echo "Starting Dash Graphing Tool Setup..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "ERROR: Python $REQUIRED_VERSION or higher is required. Found Python $PYTHON_VERSION"
    exit 1
fi

echo "SUCCESS: Python $PYTHON_VERSION detected"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "SUCCESS: Virtual environment created"
else
    echo "SUCCESS: Virtual environment found"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "SUCCESS: Dependencies installed successfully"

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "ERROR: app.py not found in current directory"
    exit 1
fi

echo "Starting Dash Graphing Tool..."
echo "The application will be available at: http://localhost:8050"
echo "To access from other devices, use: http://$(hostname -I | awk '{print $1}'):8050"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the application
python app.py
