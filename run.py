import subprocess
import os
import sys
import time
import socket

class ProjectManager:
    def __init__(self):
        # استبدل هذه المسارات بالمسارات الفعلية لمشاريعك
        self.projects = {
            "django": {
                "path": r"mm",  # استبدل بمسار Django
                "command": ["python", "manage.py", "runserver"],
                "port": 8000,
                "name": "Django Web Server"
            },
            "telegram_bot": {
                "path": r"telegramBot/ichancyBot",
                "command": ["python", "-m", "bot"],  # أو ["python", "bot.py"] حسب التركيب
                "name": "Telegram Bot"
            }
        }
    
    def check_port(self, port):
        """فحص إذا كان المنفذ مشغول"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                return s.connect_ex(('localhost', port)) == 0
        except:
            return False
    
    def run_django(self):
        """تشغيل مشروع Django"""
        project = self.projects["django"]
        
        if not os.path.exists(project["path"]):
            print(f"❌ مسار {project['name']} غير موجود: {project['path']}")
            return False
        
        # فحص المنفذ
        if self.check_port(project["port"]):
            print(f"🔄 المنفذ {project['port']} مشغول، جرب منفذ {project['port'] + 1}")
            command = ["python", "manage.py", "runserver", str(project["port"] + 1)]
        else:
            command = project["command"]
        
        try:
            print(f"🚀 تشغيل {project['name']}...")
            process = subprocess.Popen(
                ['cmd', '/k'] + command,
                cwd=project["path"],
                shell=True
            )
            
            time.sleep(5)  # انتظار حتى يكتمل تشغيل Django
            
            if process.poll() is not None:
                print(f"❌ {project['name']} توقف فور التشغيل!")
                return False
            
            print(f"✅ {project['name']} يعمل بنجاح على http://localhost:{project['port']}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تشغيل {project['name']}: {e}")
            return False
    
    def run_telegram_bot(self):
        """تشغيل بوت التليجرام"""
        project = self.projects["telegram_bot"]
        
        if not os.path.exists(project["path"]):
            print(f"❌ مسار {project['name']} غير موجود: {project['path']}")
            return False
        
        # عدة احتمالات لتنفيذ البوت
        possible_commands = [
            ["python", "-m", "bot"],           # إذا كان bot عبارة عن package
            ["python", "bot.py"],              # إذا كان ملف مباشر
            ["python", "main.py"],             # إذا كان اسم الملف main.py
            ["python", "ichancyBot/bot.py"]    # إذا كان المسار مختلف
        ]
        
        for command in possible_commands:
            try:
                print(f"🤖 تشغيل {project['name']}...")
                process = subprocess.Popen(
                    ['cmd', '/k'] + command,
                    cwd=project["path"],
                    shell=True
                )
                
                time.sleep(3)
                
                if process.poll() is None:  # لا يزال يعمل
                    print(f"✅ {project['name']} يعمل بنجاح!")
                    return True
                    
            except Exception as e:
                print(f"⚠️  محاولة فاشلة بالأمر {command}: {e}")
                continue
        
        print(f"❌ فشل جميع محاولات تشغيل {project['name']}")
        return False
    
    def run_all(self):
        """تشغيل جميع المشاريع"""
        print("🎯 بدء تشغيل المشاريع...")
        print("=" * 50)
        
        # تشغيل Django أولاً
        django_success = self.run_django()
        
        # ثم تشغيل البوت
        time.sleep(2)
        bot_success = self.run_telegram_bot()
        
        print("=" * 50)
        if django_success and bot_success:
            print("✅ تم تشغيل جميع المشاريع بنجاح!")
        else:
            print("⚠️  بعض المشاريع قد لا تعمل بشكل صحيح")
        
        self.show_instructions()
    
    def show_instructions(self):
        """عرض تعليمات للمستخدم"""
        print("\n📋 تعليمات التشغيل:")
        print("- لرؤية موقع Django: http://localhost:8000")
        print("- لإيقاف Django: اضغط CTRL+C في نافذة Django")
        print("- لإيقاف البوت: اضغط CTRL+C في نافذة البوت")
        print("- لإغلاق جميع المشاريع: أغلق نوافذ الأوامر يدوياً")

def main():
    manager = ProjectManager()
    manager.run_all()
if __name__ == "__main__":
    main()