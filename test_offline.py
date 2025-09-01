#!/usr/bin/env python3
"""
Offline Test Script for Graphing Tool
This script tests if the application can run completely offline.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available locally."""
    print("🔍 Checking local dependencies...")
    
    # Check if local files exist
    local_files = [
        "static/js/lib/plotly-latest.min.js",
        "static/css/style.css",
        "static/css/icons.css",
        "static/js/app.js",
        "templates/index.html",
        "static/images/icons/chart-line.svg",
        "static/images/icons/cloud-upload.svg",
        "static/images/icons/folder-open.svg",
        "static/images/icons/settings.svg",
        "static/images/icons/refresh.svg",
        "static/images/icons/chart-bar.svg",
        "static/images/icons/info-circle.svg",
        "static/images/icons/columns.svg",
        "static/images/icons/palette.svg",
        "static/images/icons/ruler.svg",
        "static/images/icons/magic.svg",
        "static/images/icons/chart-area.svg",
        "static/images/icons/download.svg",
        "static/images/icons/expand.svg"
    ]
    
    missing_files = []
    for file_path in local_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All local dependencies found!")
    return True

def test_offline_startup():
    """Test if the Flask app can start without internet."""
    print("\n🚀 Testing offline startup...")
    
    try:
        # Try to import required modules
        import flask
        import pandas
        import plotly
        print("✅ All Python dependencies available")
        
        # Test if we can start the app
        result = subprocess.run([
            sys.executable, "-c", 
            "from app import app; print('✅ Flask app imports successfully')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Flask app can start offline")
            return True
        else:
            print(f"❌ Flask app startup failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Offline startup test failed: {e}")
        return False

def check_internet_dependencies():
    """Check if there are any remaining internet dependencies."""
    print("\n🌐 Checking for internet dependencies...")
    
    # Read HTML template to check for CDN links
    try:
        with open("templates/index.html", "r") as f:
            html_content = f.read()
        
        cdn_patterns = [
            "https://",
            "http://",
            "cdn.",
            "//cdn."
        ]
        
        found_cdn = []
        for pattern in cdn_patterns:
            if pattern in html_content:
                found_cdn.append(pattern)
        
        if found_cdn:
            print(f"⚠️  Found potential CDN references: {found_cdn}")
            return False
        else:
            print("✅ No CDN references found in HTML")
            return True
            
    except Exception as e:
        print(f"❌ Error checking HTML: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 50)
    print("🌐 OFFLINE CAPABILITY TEST")
    print("=" * 50)
    
    # Check local dependencies
    deps_ok = check_dependencies()
    
    # Check for internet dependencies
    no_cdn = check_internet_dependencies()
    
    # Test offline startup
    startup_ok = test_offline_startup()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    if deps_ok and no_cdn and startup_ok:
        print("🎉 SUCCESS: Application is fully offline-capable!")
        print("\n✅ You can run this application without internet:")
        print("   - All dependencies are local")
        print("   - Custom SVG icons for offline use")
        print("   - No CDN references")
        print("   - Flask server starts offline")
        print("\n🚀 To start: python3 app.py")
    else:
        print("❌ FAILED: Application has internet dependencies")
        if not deps_ok:
            print("   - Missing local files")
        if not no_cdn:
            print("   - CDN references found")
        if not startup_ok:
            print("   - Flask startup issues")

if __name__ == "__main__":
    main()
