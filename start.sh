#!/bin/bash

echo "Starting CSV Graph Generator..."
echo "Installing dependencies if needed..."

source venv/bin/activate
# Install dependencies
pip3 install -r requirements.txt

# Start the Flask application
python3 app.py
/usr/bin/firefox http://localhost:5001 &

echo "Starting the application..."
echo "Access the application at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo ""