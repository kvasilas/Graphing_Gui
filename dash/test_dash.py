#!/usr/bin/env python3
"""
Test script for the Dash Graphing Tool
This script verifies that all dependencies are available and the app can start
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'dash',
        'dash_bootstrap_components', 
        'pandas',
        'plotly',
        'numpy'
    ]
    
    print("Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages imported successfully!")
        return True

def test_app_creation():
    """Test if the Dash app can be created"""
    try:
        from app import app
        print("✅ Dash app created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create Dash app: {e}")
        return False

def test_plotly_version():
    """Test Plotly version compatibility"""
    try:
        import plotly
        import plotly.graph_objects as go
        
        version = plotly.__version__
        print(f"✅ Plotly version: {version}")
        
        # Check if Scattermap is available (requires 5.24+)
        if hasattr(go, 'Scattermap'):
            print("✅ Scattermap available for map visualizations")
        else:
            print("⚠️ Scattermap not available - map features may be limited")
            print("   Consider upgrading Plotly: pip install plotly>=5.24")
        
        return True
    except Exception as e:
        print(f"❌ Plotly test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Dash Graphing Tool Setup")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("App Creation", test_app_creation),
        ("Plotly Compatibility", test_plotly_version)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! The Dash app is ready to run.")
        print("   Start the app with: python app.py")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues before running the app.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
