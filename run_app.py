#!/usr/bin/env python3
"""
Startup script for EcoSolvE platform
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "models",
        "data",
        "logs",
        "exports",
        "uploads"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def check_config():
    """Check configuration files"""
    config_files = ["config.py", "utils.py"]
    for file in config_files:
        if not os.path.exists(file):
            print(f"❌ Missing configuration file: {file}")
            return False
    print("✅ Configuration files found")
    return True

def run_application():
    """Run the Streamlit application"""
    print("🚀 Starting EcoSolvE application...")
    print("🌐 The application will be available at: http://localhost:8501")
    print("📱 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Set environment variables for better performance
        env = os.environ.copy()
        env["STREAMLIT_SERVER_PORT"] = "8501"
        env["STREAMLIT_SERVER_ADDRESS"] = "localhost"
        env["STREAMLIT_SERVER_HEADLESS"] = "true"
        env["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
        env["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
        
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], env=env)
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main startup function"""
    print("🌍 EcoSolvE - Intelligent Solvent Prediction Platform")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check configuration
    if not check_config():
        print("❌ Configuration check failed")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies if needed
    if "--install-deps" in sys.argv:
        if not install_dependencies():
            sys.exit(1)
    
    # Run the application
    run_application()

if __name__ == "__main__":
    main()
