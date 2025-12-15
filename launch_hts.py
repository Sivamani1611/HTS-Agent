#!/usr/bin/env python3
"""
HTS AI Agent - Simplified Launch Script
Quick launcher for the cleaned up HTS Agent project
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

class HTSLauncher:
    """Simple launcher for HTS Agent applications"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "hts_agent_env"
        self.python_exe = self.venv_path / "Scripts" / "python.exe"
        
        # Check if we're in virtual environment
        if not self.python_exe.exists():
            self.python_exe = sys.executable
    
    def print_banner(self):
        """Print launcher banner"""
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║    🚀 HTS AI AGENT - SIMPLIFIED LAUNCHER                               ║
║                                                                          ║
║    Quick access to enhanced trade intelligence tools                     ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)
    
    def launch_web_app(self, app_type="ultimate"):
        """Launch web application"""
        apps = {
            "ultimate": "app_ultimate.py",
            "working": "app_working.py"
        }
        
        app_file = apps.get(app_type, "app_ultimate.py")
        
        if not (self.project_root / app_file).exists():
            print(f"❌ Error: {app_file} not found!")
            return False
        
        print(f"🚀 Launching {app_type.title()} Web Application...")
        print(f"📱 File: {app_file}")
        print("🌐 URL: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop")
        print("-" * 60)
        
        try:
            # Kill existing streamlit processes
            self.stop_streamlit()
            
            # Change to project directory and run
            os.chdir(self.project_root)
            subprocess.run([str(self.python_exe), "-m", "streamlit", "run", app_file])
            
        except KeyboardInterrupt:
            print("\n🛑 Application stopped by user")
        except FileNotFoundError:
            print("❌ Streamlit not found. Please install: pip install streamlit")
        except Exception as e:
            print(f"❌ Error launching app: {e}")
        
        return True
    
    def launch_cli(self, mode="enhanced"):
        """Launch CLI application"""
        cli_apps = {
            "enhanced": "main_fixed.py",
            "interactive": "cli_simple.py"
        }
        
        cli_file = cli_apps.get(mode, "main_fixed.py")
        
        if not (self.project_root / cli_file).exists():
            print(f"❌ Error: {cli_file} not found!")
            return False
        
        print(f"💻 Launching {mode.title()} CLI...")
        print(f"📁 File: {cli_file}")
        print("-" * 60)
        
        try:
            os.chdir(self.project_root)
            if mode == "interactive":
                # Run interactive CLI directly
                subprocess.run([str(self.python_exe), cli_file])
            else:
                # Show enhanced CLI help and run interactively
                subprocess.run([str(self.python_exe), cli_file, "--chat"])
                
        except KeyboardInterrupt:
            print("\n🛑 CLI stopped by user")
        except Exception as e:
            print(f"❌ Error launching CLI: {e}")
        
        return True
    
    def stop_streamlit(self):
        """Stop existing Streamlit processes"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/f', '/im', 'streamlit.exe'], 
                             capture_output=True, text=True)
            else:  # Linux/Mac
                subprocess.run(['pkill', '-f', 'streamlit'], 
                             capture_output=True, text=True)
        except:
            pass  # Ignore errors if no processes found
    
    def show_status(self):
        """Show project status"""
        print("📊 HTS Agent Project Status")
        print("=" * 40)
        
        # Check important files
        files_to_check = [
            ("app_ultimate.py", "Ultimate Web App"),
            ("app_working.py", "Working Web App"),
            ("main_fixed.py", "Enhanced CLI"),
            ("cli_simple.py", "Interactive CLI"),
            ("manage_project.py", "Project Manager")
        ]
        
        print("\n📁 Available Applications:")
        for filename, description in files_to_check:
            path = self.project_root / filename
            if path.exists():
                size = path.stat().st_size // 1024  # KB
                print(f"✅ {description:<20} {filename:<20} ({size} KB)")
            else:
                print(f"❌ {description:<20} {filename:<20} MISSING")
        
        # Check Python environment
        print(f"\n🐍 Python Environment:")
        print(f"✅ Python: {self.python_exe}")
        print(f"✅ Working Directory: {self.project_root}")
        
        # Check key packages
        key_packages = ["streamlit", "pandas", "plotly"]
        print(f"\n📦 Key Packages:")
        for package in key_packages:
            try:
                result = subprocess.run([str(self.python_exe), "-c", f"import {package}; print({package}.__version__)"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    print(f"✅ {package:<15} v{version}")
                else:
                    print(f"❌ {package:<15} NOT INSTALLED")
            except:
                print(f"❌ {package:<15} CHECK FAILED")
    
    def quick_demo(self):
        """Run a quick demonstration"""
        print("🎯 HTS Agent Quick Demo")
        print("=" * 30)
        
        print("\n1. Testing Enhanced CLI...")
        try:
            result = subprocess.run([
                str(self.python_exe), "main_fixed.py", 
                "--query", "What is GSP?"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ CLI Query Test: PASSED")
                print("📝 Response preview:", result.stdout[:100] + "...")
            else:
                print("❌ CLI Query Test: FAILED")
        except:
            print("❌ CLI Query Test: ERROR")
        
        print("\n2. Testing Interactive CLI...")
        print("💡 Tip: Run 'python launch_hts.py --cli interactive' to test interactively")
        
        print("\n3. Web Apps Available:")
        print("🌐 Ultimate App: python launch_hts.py --web ultimate")
        print("🔧 Working App: python launch_hts.py --web working")
        
        print("\n✅ Demo completed! Use the commands above to launch applications.")

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description='HTS AI Agent - Simplified Launcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python launch_hts.py --web ultimate     # Launch ultimate web app
  python launch_hts.py --web working      # Launch working web app
  python launch_hts.py --cli enhanced     # Launch enhanced CLI
  python launch_hts.py --cli interactive  # Launch interactive CLI
  python launch_hts.py --status           # Show project status
  python launch_hts.py --demo             # Run quick demo
  python launch_hts.py --stop             # Stop all apps
        '''
    )
    
    parser.add_argument('--web', choices=['ultimate', 'working'], 
                       help='Launch web application')
    parser.add_argument('--cli', choices=['enhanced', 'interactive'], 
                       help='Launch CLI application')
    parser.add_argument('--status', action='store_true', 
                       help='Show project status')
    parser.add_argument('--demo', action='store_true', 
                       help='Run quick demonstration')
    parser.add_argument('--stop', action='store_true', 
                       help='Stop all running applications')
    
    args = parser.parse_args()
    launcher = HTSLauncher()
    
    # Always show banner
    launcher.print_banner()
    
    if args.web:
        launcher.launch_web_app(args.web)
    elif args.cli:
        launcher.launch_cli(args.cli)
    elif args.status:
        launcher.show_status()
    elif args.demo:
        launcher.quick_demo()
    elif args.stop:
        launcher.stop_streamlit()
        print("🛑 Stopped all applications")
    else:
        # Interactive menu
        print("🎯 HTS Agent Launcher Menu")
        print("=" * 30)
        
        while True:
            print("""
Available Options:
1. 🌐 Launch Ultimate Web App
2. 🔧 Launch Working Web App  
3. 💻 Launch Enhanced CLI
4. 🗣️  Launch Interactive CLI
5. 📊 Show Status
6. 🎯 Quick Demo
7. 🛑 Stop All Apps
8. ❌ Exit

""")
            
            try:
                choice = input("Enter your choice (1-8): ").strip()
                
                if choice == '1':
                    launcher.launch_web_app('ultimate')
                elif choice == '2':
                    launcher.launch_web_app('working')
                elif choice == '3':
                    launcher.launch_cli('enhanced')
                elif choice == '4':
                    launcher.launch_cli('interactive')
                elif choice == '5':
                    launcher.show_status()
                elif choice == '6':
                    launcher.quick_demo()
                elif choice == '7':
                    launcher.stop_streamlit()
                    print("🛑 Stopped all applications")
                elif choice == '8':
                    print("👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-8.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 