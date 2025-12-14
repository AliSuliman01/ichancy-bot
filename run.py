import subprocess
import os
import sys
import time
import socket

class ProjectManager:
    def __init__(self):
        # Replace these paths with the actual paths of your projects
        self.projects = {
            "django": {
                "path": r"mm",  # Replace with Django path
                "command": ["python", "manage.py", "runserver"],
                "port": 8000,
                "name": "Django Web Server"
            },
            "telegram_bot": {
                "path": r"telegramBot/ichancyBot",
                "command": ["python", "-m", "bot"],  # or ["python", "bot.py"] depending on structure
                "name": "Telegram Bot"
            }
        }
    
    def check_port(self, port):
        """Check if the port is busy"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                return s.connect_ex(('localhost', port)) == 0
        except:
            return False
    
    def run_django(self):
        """Run Django project"""
        project = self.projects["django"]
        
        if not os.path.exists(project["path"]):
            print(f"❌ Path for {project['name']} not found: {project['path']}")
            return False
        
        # Check port
        if self.check_port(project["port"]):
            print(f"🔄 Port {project['port']} is busy, trying port {project['port'] + 1}")
            command = ["python", "manage.py", "runserver", str(project["port"] + 1)]
        else:
            command = project["command"]
        
        try:
            print(f"🚀 Starting {project['name']}...")
            
            # First validate the command
            test_process = subprocess.Popen(
                command,
                cwd=project["path"],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(2)  # Wait a bit to check for immediate errors
            
            if test_process.poll() is not None:
                # Process exited immediately - there's an error
                stdout, stderr = test_process.communicate()
                if stderr:
                    print(f"❌ Error: {stderr[:500]}")
                if stdout:
                    print(f"Output: {stdout[:200]}")
                print(f"❌ {project['name']} stopped immediately after starting!")
                return False
            
            # If we get here, Django is starting successfully
            # Now start it in a new console window
            subprocess.Popen(
                command,
                cwd=project["path"],
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )
            
            # Close the test process
            test_process.terminate()
            try:
                test_process.wait(timeout=1)
            except:
                test_process.kill()
            
            time.sleep(3)  # Wait for Django to fully start
            
            print(f"✅ {project['name']} is running successfully on http://localhost:{project['port']}")
            return True
            
        except Exception as e:
            print(f"❌ Error starting {project['name']}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_telegram_bot(self):
        """Run Telegram bot"""
        project = self.projects["telegram_bot"]
        
        if not os.path.exists(project["path"]):
            print(f"❌ Path for {project['name']} not found: {project['path']}")
            return False
        
        # Several possibilities to run the bot
        possible_commands = [
            # ["python", "-m", "bot"],           # If bot is a package
            ["python", "bot.py"],              # If it's a direct file
            # ["python", "ichancyBot/bot.py"]    # If the path is different
        ]
        
        for command in possible_commands:
            try:
                print(f"🤖 Starting {project['name']}...")
                
                # Create a temporary error log file to capture startup errors
                error_log = os.path.join(project["path"], "startup_error.log")
                
                # Open error log file (keep it open while process runs)
                err_file = open(error_log, 'w')
                
                # Start the process in a new console window
                # Redirect stderr to a file so we can check for errors
                process = subprocess.Popen(
                    command,
                    cwd=project["path"],
                    shell=True,
                    stderr=err_file,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
                )
                
                # Wait a bit to see if process starts successfully
                time.sleep(3)
                
                # Close the error file so we can read it
                err_file.close()
                
                # Check if process is still running
                if process.poll() is None:  # Still running
                    print(f"✅ {project['name']} is running successfully!")
                    # Clean up error log if successful
                    if os.path.exists(error_log):
                        try:
                            os.remove(error_log)
                        except:
                            pass
                    return True
                else:
                    # Process exited, check error log
                    if os.path.exists(error_log):
                        try:
                            with open(error_log, 'r') as f:
                                error_content = f.read()
                                if error_content:
                                    print(f"❌ Error starting bot:")
                                    print(error_content[:500])  # Show first 500 chars
                            os.remove(error_log)
                        except Exception as e:
                            print(f"⚠️  Could not read error log: {e}")
                    print(f"⚠️  Process exited with code {process.returncode}")
                    continue
                    
            except Exception as e:
                print(f"⚠️  Failed attempt with command {command}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"❌ All attempts to start {project['name']} failed")
        return False
    
    def run_all(self):
        """Run all projects"""
        print("🎯 Starting projects...")
        print("=" * 50)
        
        # Run Django first
        # django_success = self.run_django()
        django_success = True
        
        # Then run the bot
        time.sleep(2)
        bot_success = self.run_telegram_bot()
        
        print("=" * 50)
        if django_success and bot_success:
            print("✅ All projects started successfully!")
        else:
            print("⚠️  Some projects may not be working correctly")
        
        self.show_instructions()
    
    def show_instructions(self):
        """Show instructions to the user"""
        print("\n📋 Running Instructions:")
        print("- To view Django site: http://localhost:8000")
        print("- To stop Django: Press CTRL+C in Django window")
        print("- To stop the bot: Press CTRL+C in bot window")
        print("- To close all projects: Manually close command windows")

def main():
    manager = ProjectManager()
    manager.run_all()
if __name__ == "__main__":
    main()