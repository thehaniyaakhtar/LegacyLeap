#!/usr/bin/env python3
"""
Simple system test for AS/400 Legacy Modernization Assistant
"""

import requests
import time
import json
import subprocess
import sys
import os
from pathlib import Path

def test_backend_connection():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running")
        return False
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        return False

def test_frontend_connection():
    """Test if frontend is running"""
    try:
        response = requests.get("http://localhost:3000/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running")
        return False
    except Exception as e:
        print(f"❌ Frontend test error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🧪 Testing API endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print("❌ Root endpoint failed")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test dashboard endpoint
    try:
        response = requests.get("http://localhost:8000/dashboard")
        if response.status_code == 200:
            print("✅ Dashboard endpoint working")
        else:
            print("❌ Dashboard endpoint failed")
            return False
    except Exception as e:
        print(f"❌ Dashboard endpoint error: {e}")
        return False
    
    # Test file upload with sample data
    try:
        sample_data = """CUST001JOHN DOE    123 MAIN ST    NEW YORK    NY10001 555-0123
CUST002JANE SMITH  456 OAK AVE   CHICAGO     IL60601 555-0456"""
        
        files = {"file": ("test_customers.txt", sample_data, "text/plain")}
        response = requests.post("http://localhost:8000/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ File upload working")
                legacy_id = data["legacy_id"]
                
                # Test transformation
                transform_response = requests.post(f"http://localhost:8000/transform/{legacy_id}")
                if transform_response.status_code == 200:
                    transform_data = transform_response.json()
                    if transform_data.get("success"):
                        print("✅ Data transformation working")
                        return True
                    else:
                        print("❌ Data transformation failed")
                        return False
                else:
                    print("❌ Transform endpoint failed")
                    return False
            else:
                print("❌ File upload failed")
                return False
        else:
            print(f"❌ Upload endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Upload test error: {e}")
        return False

def start_backend():
    """Start backend server"""
    print("🚀 Starting backend server...")
    
    # Change to backend directory
    os.chdir("backend")
    
    try:
        # Start backend in background
        process = subprocess.Popen([sys.executable, "main.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Backend started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start: {stderr.decode()}")
            return None
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start frontend server"""
    print("🚀 Starting frontend server...")
    
    # Change to frontend directory
    os.chdir("my-legacy-modernizer")
    
    try:
        # Start frontend in background
        process = subprocess.Popen(["npm", "run", "dev"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(10)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Frontend started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start: {stderr.decode()}")
            return None
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def main():
    """Main test function"""
    print("🏆 AS/400 Legacy Modernization Assistant - System Test")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("my-legacy-modernizer"):
        print("❌ Please run this script from the project root directory")
        return False
    
    # Test if services are already running
    backend_running = test_backend_connection()
    frontend_running = test_frontend_connection()
    
    backend_process = None
    frontend_process = None
    
    # Start backend if not running
    if not backend_running:
        backend_process = start_backend()
        if not backend_process:
            print("❌ Failed to start backend")
            return False
        
        # Wait for backend to be ready
        for i in range(10):
            if test_backend_connection():
                break
            time.sleep(2)
        else:
            print("❌ Backend failed to start properly")
            return False
    
    # Start frontend if not running
    if not frontend_running:
        frontend_process = start_frontend()
        if not frontend_process:
            print("❌ Failed to start frontend")
            return False
        
        # Wait for frontend to be ready
        for i in range(15):
            if test_frontend_connection():
                break
            time.sleep(2)
        else:
            print("❌ Frontend failed to start properly")
            return False
    
    # Test API endpoints
    if not test_api_endpoints():
        print("❌ API tests failed")
        return False
    
    print("\n🎉 All tests passed! System is working correctly.")
    print("\n📍 Access URLs:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    
    print("\n⏹️ Press Ctrl+C to stop the system")
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopping system...")
        
        # Stop processes if we started them
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("✅ System stopped")
    
    return True

if __name__ == "__main__":
    main()
