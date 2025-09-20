#!/usr/bin/env python3
"""
AS/400 Legacy Modernization Assistant - Complete System Startup
"""

import os
import sys
import subprocess
import time
import threading
import requests
from pathlib import Path

class SystemManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
    
    def check_backend(self):
        """Check if backend is running"""
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_frontend(self):
        """Check if frontend is running"""
        try:
            response = requests.get("http://localhost:3000/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_backend(self):
        """Start backend server"""
        print("🚀 Starting Backend Server...")
        
        backend_dir = Path(__file__).parent / "backend"
        os.chdir(backend_dir)
        
        try:
            venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
            python_cmd = str(venv_python) if venv_python.exists() else sys.executable
            
            self.backend_process = subprocess.Popen([
                python_cmd, "-m", "uvicorn", 
                "main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000", 
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for backend to start
            for i in range(30):
                if self.check_backend():
                    print("✅ Backend started successfully")
                    return True
                time.sleep(1)
            
            print("❌ Backend failed to start")
            return False
            
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
        finally:
            os.chdir(Path(__file__).parent)
    
    def start_frontend(self):
        """Start frontend server"""
        print("🚀 Starting Frontend Server...")
        
        frontend_dir = Path(__file__).parent / "my-legacy-modernizer"
        
        try:
            os.chdir(frontend_dir)
            
            self.frontend_process = subprocess.Popen([
                "npm", "run", "dev"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for frontend to start
            for i in range(60):
                if self.check_frontend():
                    print("✅ Frontend started successfully")
                    return True
                time.sleep(1)
            
            print("❌ Frontend failed to start")
            return False
            
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False
        finally:
            os.chdir(Path(__file__).parent)
    
    def start_system(self):
        """Start the complete system"""
        print("🏆 AS/400 Legacy Modernization Assistant")
        print("=" * 60)
        
        # Check if services are already running
        backend_running = self.check_backend()
        frontend_running = self.check_frontend()
        
        if backend_running:
            print("✅ Backend is already running")
        else:
            if not self.start_backend():
                return False
        
        if frontend_running:
            print("✅ Frontend is already running")
        else:
            if not self.start_frontend():
                return False
        
        print("\n🎉 System is ready!")
        print("📍 Frontend: http://localhost:3000")
        print("📍 Backend: http://localhost:8000")
        print("📍 API Docs: http://localhost:8000/docs")
        print("\n⏹️ Press Ctrl+C to stop the system")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️ Stopping system...")
            self.stop_system()
        
        return True
    
    def stop_system(self):
        """Stop all services"""
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("✅ System stopped")

def main():
    manager = SystemManager()
    manager.start_system()

if __name__ == "__main__":
    main()