#!/usr/bin/env python3
"""
Complete demo runner for AS/400 Legacy Modernization Assistant
"""

import subprocess
import sys
import os
import time
import webbrowser
import json
from pathlib import Path

def print_banner():
    """Print the project banner"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🏆 AS/400 Legacy Modernization Assistant 🏆                ║
║                                                                              ║
║  Transform your legacy IBM AS/400 systems into modern APIs and microservices ║
║  with the power of AI!                                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

def check_python():
    """Check Python installation"""
    print("🐍 Checking Python...")
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python: {result.stdout.strip()}")
            return True
        else:
            print("❌ Python not found")
            return False
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def check_node():
    """Check Node.js installation"""
    print("📦 Checking Node.js...")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            print("   Please install Node.js from https://nodejs.org/")
            return False
    except Exception as e:
        print(f"❌ Node.js check failed: {e}")
        return False

def install_backend_deps():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    
    if not os.path.exists("backend/requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              cwd="backend", capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Backend dependencies installed")
            return True
        else:
            print(f"❌ Backend installation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Backend installation error: {e}")
        return False

def install_frontend_deps():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    
    if not os.path.exists("my-legacy-modernizer/package.json"):
        print("❌ package.json not found")
        return False
    
    try:
        result = subprocess.run(["npm", "install"], 
                              cwd="my-legacy-modernizer", capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Frontend dependencies installed")
            return True
        else:
            print(f"❌ Frontend installation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Frontend installation error: {e}")
        return False

def create_sample_data():
    """Create sample data files"""
    print("\n📁 Creating sample data...")
    
    try:
        # Change to backend directory
        original_dir = os.getcwd()
        os.chdir("backend")
        
        # Import and run sample data creation
        from sample_data import create_sample_files
        create_sample_files()
        
        # Change back
        os.chdir(original_dir)
        
        print("✅ Sample data created")
        return True
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting backend server...")
    
    try:
        # Start backend process
        process = subprocess.Popen([sys.executable, "main.py"], 
                                 cwd="backend",
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait for startup
        print("⏳ Waiting for backend to start...")
        time.sleep(5)
        
        # Check if running
        if process.poll() is None:
            print("✅ Backend server started")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start: {stderr.decode()}")
            return None
    except Exception as e:
        print(f"❌ Backend startup error: {e}")
        return None

def start_frontend():
    """Start the frontend server"""
    print("\n🚀 Starting frontend server...")
    
    try:
        # Start frontend process
        process = subprocess.Popen(["npm", "run", "dev"], 
                                 cwd="my-legacy-modernizer",
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait for startup
        print("⏳ Waiting for frontend to start...")
        time.sleep(10)
        
        # Check if running
        if process.poll() is None:
            print("✅ Frontend server started")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start: {stderr.decode()}")
            return None
    except Exception as e:
        print(f"❌ Frontend startup error: {e}")
        return None

def test_system():
    """Test if the system is working"""
    print("\n🧪 Testing system...")
    
    import requests
    
    # Test backend
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is responding")
        else:
            print("❌ Backend not responding properly")
            return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False
    
    # Test frontend
    try:
        response = requests.get("http://localhost:3000/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is responding")
        else:
            print("❌ Frontend not responding properly")
            return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False
    
    return True

def open_browser():
    """Open browser to the application"""
    print("\n🌐 Opening browser...")
    try:
        webbrowser.open("http://localhost:3000")
        print("✅ Browser opened")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print("   Please open http://localhost:3000 manually")

def show_demo_instructions():
    """Show demo instructions"""
    print("""
🎯 DEMO INSTRUCTIONS:

1. 📁 UPLOAD LEGACY FILES:
   - Drag and drop AS/400 files onto the upload area
   - Supported formats: .txt, .dat, .sql, .rpg, .rpgle
   - Try the sample files in backend/sample_files/

2. 🤖 AI TRANSFORMATION:
   - Watch as AI analyzes your legacy data
   - See real-time progress updates
   - Get modern API specifications

3. 📊 DASHBOARD FEATURES:
   - View processing statistics
   - Monitor transformation progress
   - Explore generated APIs and microservices

4. 🔧 API EXPLORATION:
   - Visit http://localhost:8000/docs for API documentation
   - Test the generated REST APIs
   - View OpenAPI specifications

5. 🏗️ MICROSERVICES:
   - See suggested microservices architecture
   - Get Docker and Kubernetes configurations
   - Explore service decomposition

📊 SAMPLE DATA AVAILABLE:
   - Customer data (fixed-width and delimited)
   - Order processing data
   - Product/inventory data
   - Employee HR data
   - Financial accounting data
   - DB2 table definitions
   - RPG program examples
   - Green screen interfaces

🎉 ENJOY THE DEMO!
""")

def main():
    """Main demo function"""
    print_banner()
    
    # Check prerequisites
    if not check_python():
        print("\n❌ Python is required. Please install Python 3.9+")
        return False
    
    if not check_node():
        print("\n❌ Node.js is required. Please install Node.js 16+")
        return False
    
    # Install dependencies
    if not install_backend_deps():
        print("\n❌ Failed to install backend dependencies")
        return False
    
    if not install_frontend_deps():
        print("\n❌ Failed to install frontend dependencies")
        return False
    
    # Create sample data
    if not create_sample_data():
        print("\n❌ Failed to create sample data")
        return False
    
    # Start services
    backend_process = start_backend()
    if not backend_process:
        print("\n❌ Failed to start backend")
        return False
    
    frontend_process = start_frontend()
    if not frontend_process:
        print("\n❌ Failed to start frontend")
        return False
    
    # Test system
    if not test_system():
        print("\n❌ System test failed")
        return False
    
    # Open browser
    open_browser()
    
    # Show instructions
    show_demo_instructions()
    
    print("\n✅ SYSTEM READY!")
    print("📍 Frontend: http://localhost:3000")
    print("📍 Backend:  http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/docs")
    
    print("\n⏹️ Press Ctrl+C to stop the system")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopping system...")
        
        # Stop processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("✅ System stopped. Thanks for trying the demo!")

if __name__ == "__main__":
    main()
