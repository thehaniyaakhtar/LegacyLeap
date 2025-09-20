#!/usr/bin/env python3
"""
Simple frontend startup script for AS/400 Legacy Modernization Assistant
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the frontend server"""
    print("🚀 Starting AS/400 Legacy Modernization Assistant Frontend...")
    
    # Get the frontend directory
    frontend_dir = Path(__file__).parent / "my-legacy-modernizer"
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    try:
        print("🌐 Starting Next.js development server on http://localhost:3000")
        print("⏹️ Press Ctrl+C to stop the server")
        
        # Start the Next.js development server
        subprocess.run(["npm", "run", "dev"])
        
    except KeyboardInterrupt:
        print("\n✅ Frontend server stopped")
        return True
    except FileNotFoundError:
        print("❌ npm not found! Please install Node.js and npm first.")
        return False
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return False

if __name__ == "__main__":
    main()
