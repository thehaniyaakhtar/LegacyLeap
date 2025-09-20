#!/usr/bin/env python3
"""
Setup script for AS/400 Legacy Modernization Assistant
"""

import subprocess
import sys
import os

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"   Error: {e.stderr}")
        return False

def setup_backend():
    """Setup backend dependencies"""
    print("🔧 Setting up backend...")
    
    # Check if Python is available
    if not run_command("python --version"):
        print("❌ Python is not installed or not in PATH")
        return False
    
    # Create virtual environment
    if not os.path.exists("backend/venv"):
        if not run_command("python -m venv venv", cwd="backend"):
            return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", cwd="backend"):
        return False
    
    print("✅ Backend setup complete")
    return True

def setup_frontend():
    """Setup frontend dependencies"""
    print("🔧 Setting up frontend...")
    
    # Check if Node.js is available
    if not run_command("node --version"):
        print("❌ Node.js is not installed or not in PATH")
        return False
    
    # Check if npm is available
    if not run_command("npm --version"):
        print("❌ npm is not installed or not in PATH")
        return False
    
    # Install dependencies
    if not run_command("npm install", cwd="my-legacy-modernizer"):
        return False
    
    print("✅ Frontend setup complete")
    return True

def create_sample_files():
    """Create sample data files"""
    print("📁 Creating sample data files...")
    
    try:
        from backend.sample_data import create_sample_files
        create_sample_files()
        print("✅ Sample files created")
        return True
    except Exception as e:
        print(f"❌ Error creating sample files: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 AS/400 Legacy Modernization Assistant Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("my-legacy-modernizer"):
        print("❌ Please run this script from the project root directory")
        return False
    
    success = True
    
    # Setup backend
    if not setup_backend():
        success = False
    
    # Setup frontend
    if not setup_frontend():
        success = False
    
    # Create sample files
    if not create_sample_files():
        success = False
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\nTo start the system:")
        print("1. Run: python demo.py (for demo)")
        print("2. Or run: start.bat (Windows) or ./start.sh (Linux/Mac)")
        print("3. Or manually:")
        print("   - Backend: cd backend && python main.py")
        print("   - Frontend: cd my-legacy-modernizer && npm run dev")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    main()
