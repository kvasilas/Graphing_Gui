#!/bin/bash
# Deployment Setup Script for Graph Generator
# This script sets up a virtual environment and installs all dependencies

echo "🚀 Setting up Graph Generator virtual environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version (need 3.8+ for pandas 2.1.1)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION detected. Python 3.8+ is required for pandas 2.1.1"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Verify installation
echo "🔍 Verifying installation..."
python3 -c "
import flask
import numpy
import pandas
import plotly
import werkzeug
print('✅ All packages installed successfully!')
print(f'Flask: {flask.__version__}')
print(f'NumPy: {numpy.__version__}')
print(f'Pandas: {pandas.__version__}')
print(f'Plotly: {plotly.__version__}')
print(f'Werkzeug: {werkzeug.__version__}')
"

echo ""
echo "🎉 Setup complete! To activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "🚀 To run the application:"
echo "   python3 app.py"
echo ""
echo "🌐 Access at: http://localhost:5001"
