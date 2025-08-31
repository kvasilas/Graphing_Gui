#!/bin/bash

echo "Starting CSV Graph Generator..."
echo "Installing dependencies if needed..."

# Install dependencies
python3 -m pip install flask pandas plotly werkzeug python-dotenv

echo "Starting the application..."
echo "Access the application at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 app.py
