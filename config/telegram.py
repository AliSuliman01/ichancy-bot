import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# SESSION_FILE = 'ichancy_sessions.json'
COOKIE_STRING = os.getenv('ICHANCY_COOKIE')
# Validate bot token