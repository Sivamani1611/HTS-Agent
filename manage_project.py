#!/usr/bin/env python3
"""
HTS AI Agent - Project Management Console
Comprehensive management tool for the entire HTS Agent project
"""

import os
import sys
import subprocess
import json
import argparse
from datetime import datetime
from pathlib import Path

class HTSProjectManager:
    """Comprehensive project manager for HTS Agent"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "hts_agent_env"
        self.python_exe = self.venv_path / "Scripts" / "python.exe"
        self.pip_exe = self.venv_path / "Scripts" / "pip.exe"
        
    def print_banner(self):
        """Print management console banner"""
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║    🚀 HTS AI AGENT - PROJECT MANAGEMENT CONSOLE                        ║
║                                                                          ║
║    Comprehensive management tool for the entire project                  ║
║    Deploy, Monitor, Test, and Maintain with ease                        ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)
    
    def check_environment(self):
        """Check and report environment status"""
        print("🔍 Checking Environment Status...")
        print("=" * 60)
        
        status = {
            "virtual_env": self.venv_path.exists(),
            "python": self.python_exe.exists(),
            "pip": self.pip_exe.exists(),
            "streamlit_installed": self.check_package("streamlit"),
            "plotly_installed": self.check_package("plotly"),
            "pandas_installed": self.check_package("pandas"),
        }
        
        for key, value in status.items():
            icon = "✅" if value else "❌"
            print(f"{icon} {key.replace('_', ' ').title()}: {'OK' if value else 'MISSING'}")
        
        print("=" * 60)
        return all(status.values())
    
    def check_package(self, package_name):
        """Check if a package is installed"""
        try:
            if self.python_exe.exists():
                result = subprocess.run([str(self.python_exe), "-c", f"import {package_name}"], 
                                      capture_output=True, text=True)
                return result.returncode == 0
            return False
        except:
            return False
    
    def setup_environment(self):
        """Set up the complete environment"""
        print("🛠️ Setting up environment...")
        
        # Create virtual environment if not exists
        if not self.venv_path.exists():
            print("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)])
        
        # Install essential packages
        essential_packages = [
            "streamlit>=1.29.0",
            "pandas>=2.1.1", 
            "numpy>=1.24.0",
            "plotly>=5.17.0"
        ]
        
        for package in essential_packages:
            if not self.check_package(package.split(">=")[0]):
                print(f"Installing {package}...")
                subprocess.run([str(self.pip_exe), "install", package])
        
        print("✅ Environment setup complete!")
    
    def run_app(self, app_type="ultimate"):
        """Run the specified application type"""
        app_files = {
            "ultimate": "app_ultimate.py",
            "working": "app_working.py"
        }
        
        app_file = app_files.get(app_type, "app_ultimate.py")
        
        if not (self.project_root / app_file).exists():
            print(f"❌ Application file {app_file} not found!")
            return
        
        print(f"🚀 Starting {app_type} web application...")
        print(f"📱 URL: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop")
        
        # Stop any existing Streamlit processes first
        self.stop_streamlit()
        
        # Start new Streamlit app
        try:
            subprocess.run([str(self.python_exe), "-m", "streamlit", "run", app_file])
        except KeyboardInterrupt:
            print("\n🛑 Application stopped by user")
    
    def run_cli(self, mode="enhanced"):
        """Run CLI application"""
        cli_files = {
            "enhanced": "main_fixed.py",
            "interactive": "cli_simple.py"
        }
        
        cli_file = cli_files.get(mode, "main_fixed.py")
        
        if not (self.project_root / cli_file).exists():
            print(f"❌ CLI file {cli_file} not found!")
            return
        
        print(f"💻 Starting {mode} CLI...")
        
        if mode == "interactive":
            subprocess.run([str(self.python_exe), cli_file])
        else:
            subprocess.run([str(self.python_exe), cli_file, "--help"])
    
    def stop_streamlit(self):
        """Stop all Streamlit processes"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(["taskkill", "/F", "/IM", "streamlit.exe"], 
                             capture_output=True)
            else:  # Unix/Linux
                subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
            print("🛑 Stopped existing Streamlit processes")
        except:
            pass
    
    def run_tests(self):
        """Run project tests"""
        print("🧪 Running project tests...")
        
        # Test CLI functionality
        print("\n📋 Testing CLI functionality...")
        test_commands = [
            [str(self.python_exe), "main_fixed.py", "--query", "What is GSP?"],
            [str(self.python_exe), "main_fixed.py", "--calc", "0101.30.00.00", "10000", "500", "100"],
            [str(self.python_exe), "main_fixed.py", "--list"]
        ]
        
        for cmd in test_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ {' '.join(cmd[2:])}: PASSED")
                else:
                    print(f"❌ {' '.join(cmd[2:])}: FAILED")
            except subprocess.TimeoutExpired:
                print(f"⏰ {' '.join(cmd[2:])}: TIMEOUT")
            except Exception as e:
                print(f"❌ {' '.join(cmd[2:])}: ERROR - {e}")
        
        # Test environment imports
        print("\n📦 Testing package imports...")
        test_imports = ["streamlit", "pandas", "numpy", "plotly", "json", "datetime"]
        
        for package in test_imports:
            try:
                result = subprocess.run([str(self.python_exe), "-c", f"import {package}; print('OK')"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {package}: IMPORTED")
                else:
                    print(f"❌ {package}: FAILED")
            except:
                print(f"❌ {package}: ERROR")
        
        print("\n🧪 Test completed!")
    
    def project_status(self):
        """Show comprehensive project status"""
        print("📊 Project Status Report")
        print("=" * 60)
        
        # File status
        important_files = [
            "main_fixed.py", "cli_simple.py", "app_ultimate.py", 
            "app_working.py", "requirements_basic.txt", "README.md"
        ]
        
        print("\n📁 Important Files:")
        for file in important_files:
            path = self.project_root / file
            if path.exists():
                size = path.stat().st_size / 1024  # KB
                print(f"✅ {file:<20} {size:>8.1f} KB")
            else:
                print(f"❌ {file:<20} MISSING")
        
        # Directory status
        important_dirs = ["hts_agent_env", "data", "logs", "config", "tools"]
        
        print("\n📂 Important Directories:")
        for dir_name in important_dirs:
            path = self.project_root / dir_name
            if path.exists():
                try:
                    items = len(list(path.iterdir()))
                    print(f"✅ {dir_name:<20} {items:>8} items")
                except:
                    print(f"✅ {dir_name:<20} EXISTS")
            else:
                print(f"❌ {dir_name:<20} MISSING")
        
        # Process status
        print("\n🔄 Running Processes:")
        try:
            if os.name == 'nt':
                result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq streamlit.exe"], 
                                      capture_output=True, text=True)
                if "streamlit.exe" in result.stdout:
                    print("✅ Streamlit app is running")
                else:
                    print("❌ Streamlit app is not running")
            else:
                result = subprocess.run(["pgrep", "-f", "streamlit"], capture_output=True)
                if result.returncode == 0:
                    print("✅ Streamlit app is running")
                else:
                    print("❌ Streamlit app is not running")
        except:
            print("❓ Cannot check process status")
        
        print("=" * 60)
    
    def clean_project(self):
        """Clean up project files"""
        print("🧹 Cleaning project...")
        
        # Remove temporary files
        temp_patterns = ["*.pyc", "__pycache__", ".streamlit", "*.log"]
        cleaned = 0
        
        for pattern in temp_patterns:
            for file in self.project_root.rglob(pattern):
                try:
                    if file.is_file():
                        file.unlink()
                        cleaned += 1
                    elif file.is_dir():
                        import shutil
                        shutil.rmtree(file)
                        cleaned += 1
                except:
                    pass
        
        print(f"✅ Cleaned {cleaned} temporary files/directories")
    
    def create_launcher_script(self):
        """Create a simple launcher script"""
        launcher_content = '''@echo off
echo HTS AI Agent - Quick Launcher
echo ===============================
echo.
echo Choose an option:
echo 1. Run Enhanced Web App
echo 2. Run CLI (Interactive)
echo 3. Run CLI (Single Query)
echo 4. Check Status
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting Enhanced Web App...
    hts_agent_env\\Scripts\\python.exe -m streamlit run app_fixed.py
) else if "%choice%"=="2" (
    echo Starting Interactive CLI...
    hts_agent_env\\Scripts\\python.exe cli_simple.py
) else if "%choice%"=="3" (
    set /p query="Enter your question: "
    hts_agent_env\\Scripts\\python.exe main_fixed.py --query "%query%"
    pause
) else if "%choice%"=="4" (
    hts_agent_env\\Scripts\\python.exe manage_project.py --status
    pause
) else if "%choice%"=="5" (
    exit
) else (
    echo Invalid choice!
    pause
)
'''
        
        with open(self.project_root / "launcher.bat", "w") as f:
            f.write(launcher_content)
        
        print("✅ Created launcher.bat")
    
    def quick_demo(self):
        """Run a quick demonstration"""
        print("🎯 Running Quick Demo...")
        print("=" * 40)
        
        # Demo CLI
        print("\n💻 CLI Demo:")
        demo_commands = [
            ("Question about GSP", ["--query", "What is GSP?"]),
            ("Duty Calculation", ["--calc", "0101.30.00.00", "10000", "500", "100"]),
            ("List HTS Codes", ["--list"])
        ]
        
        for description, args in demo_commands:
            print(f"\n🔸 {description}:")
            try:
                result = subprocess.run([str(self.python_exe), "main_fixed.py"] + args, 
                                      capture_output=True, text=True, timeout=10)
                print(result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n🎯 Demo completed!")

def main():
    """Main management function"""
    parser = argparse.ArgumentParser(
        description='HTS AI Agent Project Management Console',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--setup', action='store_true', help='Set up environment')
    parser.add_argument('--status', action='store_true', help='Show project status')
    parser.add_argument('--run-app', choices=['ultimate', 'working'], 
                       help='Run web application')
    parser.add_argument('--run-cli', choices=['enhanced', 'interactive'], 
                       help='Run CLI application')
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--clean', action='store_true', help='Clean temporary files')
    parser.add_argument('--launcher', action='store_true', help='Create launcher script')
    parser.add_argument('--demo', action='store_true', help='Run quick demo')
    parser.add_argument('--stop', action='store_true', help='Stop all running apps')
    
    args = parser.parse_args()
    manager = HTSProjectManager()
    
    manager.print_banner()
    
    if args.setup:
        manager.setup_environment()
    elif args.status:
        manager.check_environment()
        manager.project_status()
    elif args.run_app:
        manager.run_app(args.run_app)
    elif args.run_cli:
        manager.run_cli(args.run_cli)
    elif args.test:
        manager.run_tests()
    elif args.clean:
        manager.clean_project()
    elif args.launcher:
        manager.create_launcher_script()
    elif args.demo:
        manager.quick_demo()
    elif args.stop:
        manager.stop_streamlit()
        print("🛑 Stopped all applications")
    else:
        # Interactive menu
        print("🎯 Interactive Management Console")
        print("=" * 40)
        
        while True:
            print("""
Available Commands:
1. 🛠️  Setup Environment
2. 📊 Check Status  
3. 🚀 Run Ultimate Web App
4. 🔧 Run Working Web App
5. 💻 Run Enhanced CLI
6. 🗣️  Run Interactive CLI
7. 🧪 Run Tests
8. 🎯 Quick Demo
9. 🧹 Clean Project
10. 🛑 Stop Apps
11. ❌ Exit

""")
            
            try:
                choice = input("Enter your choice (1-11): ").strip()
                
                if choice == '1':
                    manager.setup_environment()
                elif choice == '2':
                    manager.check_environment()
                    manager.project_status()
                elif choice == '3':
                    manager.run_app('ultimate')
                elif choice == '4':
                    manager.run_app('working')
                elif choice == '5':
                    manager.run_cli('enhanced')
                elif choice == '6':
                    manager.run_cli('interactive')
                elif choice == '7':
                    manager.run_tests()
                elif choice == '8':
                    manager.quick_demo()
                elif choice == '9':
                    manager.clean_project()
                elif choice == '10':
                    manager.stop_streamlit()
                elif choice == '11':
                    print("👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice!")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    main() 