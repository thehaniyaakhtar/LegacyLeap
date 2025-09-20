#!/usr/bin/env python3
"""
AS/400 Legacy Modernization Assistant - Backend Startup Script
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    """Start the backend server"""
    print("🚀 Starting AS/400 Legacy Modernization Assistant Backend...")
    print("=" * 60)
    
    # Get the backend directory
    backend_dir = Path(__file__).parent / "backend"
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Change to backend directory
    original_dir = os.getcwd()
    os.chdir(backend_dir)
    
    try:
        # Use virtual environment python
        venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
        
        if venv_python.exists():
            python_cmd = str(venv_python)
            print(f"✅ Using virtual environment: {python_cmd}")
        else:
            python_cmd = sys.executable
            print(f"⚠️ Using system Python: {python_cmd}")
        
        # Check if FastAPI is installed
        try:
            result = subprocess.run([python_cmd, "-c", "import fastapi; print('FastAPI available')"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ FastAPI is available")
            else:
                print("❌ FastAPI not found, installing...")
                subprocess.run([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"])
        except Exception as e:
            print(f"❌ Error checking FastAPI: {e}")
            return False
        
        # Start the server
        print("\n🌐 Starting FastAPI server...")
        print("📍 Backend URL: http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🔧 Interactive API: http://localhost:8000/redoc")
        print("⏹️ Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Use uvicorn to start the server
        subprocess.run([
            python_cmd, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n✅ Backend server stopped")
        return True
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False
    finally:
        # Restore original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    main()