#!/usr/bin/env python3
"""
System startup script for AS/400 Legacy Modernization Assistant
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def run_backend():
    """Start the backend server"""
    print("🚀 Starting Backend Server...")
    os.chdir("backend")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Backend server stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Start the frontend server"""
    print("🚀 Starting Frontend Server...")
    os.chdir("my-legacy-modernizer")
    try:
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Frontend server stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python packages
    try:
        import fastapi
        import uvicorn
        import pandas
        import numpy
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Node.js OK")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    # Check npm packages
    if not os.path.exists("my-legacy-modernizer/node_modules"):
        print("❌ Frontend dependencies not installed")
        print("Run: cd my-legacy-modernizer && npm install")
        return False
    else:
        print("✅ Frontend dependencies OK")
    
    return True

def main():
    """Main startup function"""
    print("🏆 AS/400 Legacy Modernization Assistant")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("my-legacy-modernizer"):
        print("❌ Please run this script from the project root directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing dependencies.")
        return
    
    print("\n✅ All dependencies OK")
    print("\n🚀 Starting system...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend in a separate thread
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    frontend_thread.start()
    
    # Wait a moment for frontend to start
    time.sleep(5)
    
    # Open browser
    print("\n🌐 Opening browser...")
    try:
        webbrowser.open("http://localhost:3000")
    except Exception as e:
        print(f"Could not open browser: {e}")
    
    print("\n✅ System started successfully!")
    print("\n📍 URLs:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("\n⏹️ Press Ctrl+C to stop all services")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Shutting down system...")
        print("✅ System stopped")

if __name__ == "__main__":
    main()
