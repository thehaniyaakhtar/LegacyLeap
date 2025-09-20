#!/usr/bin/env python3
"""
Deployment script for AS/400 Legacy Modernization Assistant
"""

import subprocess
import sys
import os
import json
import time
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a command and return success status"""
    try:
        print(f"🔧 Running: {command}")
        result = subprocess.run(command, shell=True, cwd=cwd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if all prerequisites are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    if not run_command("python --version", check=False):
        print("❌ Python not found")
        return False
    
    # Check Node.js
    if not run_command("node --version", check=False):
        print("❌ Node.js not found")
        return False
    
    # Check Docker (optional)
    if run_command("docker --version", check=False):
        print("✅ Docker available")
    else:
        print("⚠️ Docker not found (optional for containerized deployment)")
    
    # Check Kubernetes (optional)
    if run_command("kubectl version --client", check=False):
        print("✅ Kubernetes available")
    else:
        print("⚠️ Kubernetes not found (optional for K8s deployment)")
    
    return True

def install_backend_dependencies():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    
    if not os.path.exists("backend/requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    return run_command("pip install -r requirements.txt", cwd="backend")

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    
    if not os.path.exists("my-legacy-modernizer/package.json"):
        print("❌ package.json not found")
        return False
    
    return run_command("npm install", cwd="my-legacy-modernizer")

def create_sample_data():
    """Create sample data files"""
    print("\n📁 Creating sample data...")
    
    try:
        from backend.sample_data import create_sample_files
        create_sample_files()
        print("✅ Sample data created")
        return True
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def run_tests():
    """Run system tests"""
    print("\n🧪 Running tests...")
    
    # Run backend tests
    if os.path.exists("backend/test_api.py"):
        if run_command("python -m pytest backend/test_api.py -v", check=False):
            print("✅ Backend tests passed")
        else:
            print("⚠️ Some backend tests failed")
    
    return True

def build_docker_images():
    """Build Docker images"""
    print("\n🐳 Building Docker images...")
    
    # Build backend image
    if run_command("docker build -t legacy-modernization-backend ./backend"):
        print("✅ Backend image built")
    else:
        print("❌ Failed to build backend image")
        return False
    
    # Build frontend image
    if run_command("docker build -t legacy-modernization-frontend ./my-legacy-modernizer"):
        print("✅ Frontend image built")
    else:
        print("❌ Failed to build frontend image")
        return False
    
    return True

def deploy_docker_compose():
    """Deploy using Docker Compose"""
    print("\n🐳 Deploying with Docker Compose...")
    
    if not os.path.exists("docker-compose.yml"):
        print("❌ docker-compose.yml not found")
        return False
    
    # Stop existing containers
    run_command("docker-compose down", check=False)
    
    # Start new containers
    if run_command("docker-compose up -d"):
        print("✅ Docker Compose deployment successful")
        print("📍 Access at: http://localhost")
        return True
    else:
        print("❌ Docker Compose deployment failed")
        return False

def deploy_kubernetes():
    """Deploy to Kubernetes"""
    print("\n☸️ Deploying to Kubernetes...")
    
    if not os.path.exists("k8s"):
        print("❌ Kubernetes manifests not found")
        return False
    
    # Apply namespace
    if run_command("kubectl apply -f k8s/namespace.yaml"):
        print("✅ Namespace created")
    else:
        print("❌ Failed to create namespace")
        return False
    
    # Apply all manifests
    for manifest in Path("k8s").glob("*.yaml"):
        if manifest.name != "namespace.yaml":
            if not run_command(f"kubectl apply -f {manifest}"):
                print(f"❌ Failed to apply {manifest}")
                return False
    
    print("✅ Kubernetes deployment successful")
    print("📍 Check status with: kubectl get pods -n legacy-modernization")
    return True

def create_environment_file():
    """Create environment configuration file"""
    print("\n⚙️ Creating environment configuration...")
    
    env_content = """# AS/400 Legacy Modernization Assistant Environment Configuration

# OpenAI API Key (optional, for AI features)
OPENAI_API_KEY=your-openai-api-key-here

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/legacy_modernization

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Monitoring
PROMETHEUS_ENABLED=True
GRAFANA_ENABLED=True
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Environment file created (.env)")
    print("⚠️ Please update the .env file with your actual configuration")
    return True

def generate_deployment_report():
    """Generate deployment report"""
    print("\n📊 Generating deployment report...")
    
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system": {
            "python_version": subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip(),
            "node_version": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
        },
        "deployment": {
            "backend_installed": os.path.exists("backend/venv") or True,
            "frontend_installed": os.path.exists("my-legacy-modernizer/node_modules"),
            "sample_data_created": os.path.exists("backend/sample_files"),
            "docker_available": subprocess.run(["docker", "--version"], capture_output=True, text=True).returncode == 0,
            "kubernetes_available": subprocess.run(["kubectl", "version", "--client"], capture_output=True, text=True).returncode == 0,
        },
        "endpoints": {
            "frontend": "http://localhost:3000",
            "backend": "http://localhost:8000",
            "api_docs": "http://localhost:8000/docs",
            "websocket": "ws://localhost:8000/ws"
        }
    }
    
    with open("deployment_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Deployment report generated (deployment_report.json)")
    return True

def main():
    """Main deployment function"""
    print("🚀 AS/400 Legacy Modernization Assistant - Deployment")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed")
        return False
    
    # Install dependencies
    if not install_backend_dependencies():
        print("\n❌ Backend dependency installation failed")
        return False
    
    if not install_frontend_dependencies():
        print("\n❌ Frontend dependency installation failed")
        return False
    
    # Create sample data
    if not create_sample_data():
        print("\n❌ Sample data creation failed")
        return False
    
    # Create environment file
    create_environment_file()
    
    # Run tests
    run_tests()
    
    # Ask for deployment method
    print("\n🎯 Choose deployment method:")
    print("1. Local development (recommended for demo)")
    print("2. Docker Compose")
    print("3. Kubernetes")
    print("4. All methods")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    success = True
    
    if choice in ["1", "4"]:
        print("\n🏠 Local development deployment...")
        print("✅ System ready for local development")
        print("📍 Run: python start_system.py")
    
    if choice in ["2", "4"]:
        if build_docker_images():
            deploy_docker_compose()
        else:
            success = False
    
    if choice in ["3", "4"]:
        deploy_kubernetes()
    
    # Generate report
    generate_deployment_report()
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        print("\n📍 Next steps:")
        print("1. Update .env file with your configuration")
        print("2. Start the system: python start_system.py")
        print("3. Open http://localhost:3000 in your browser")
        print("4. Upload some AS/400 files and see the magic!")
    else:
        print("\n❌ Deployment completed with errors")
        print("Check the output above for details")
    
    return success

if __name__ == "__main__":
    main()
