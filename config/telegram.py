import os
from dotenv import load_dotenv

load_dotenv()
# Bot configuration
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TRANSACTIONS_BOT_TOKEN = os.getenv('TRANSACTIONS_TELEGRAM_BOT_TOKEN')
# SESSION_FILE = 'ichancy_sessions.json'
COOKIE_STRING = os.getenv('ICHANCY_COOKIE')
COOKIE_STATUS = True
UPDATE_COOKIE_DATE:float = 2758801549.062256
COOKIE_MESSAGE_SENT = False
ACTIVE_REFRESHING_COOKIE = False
ACTIVE_REFRESHING_COOKIE_FROM_FILE = True
# Admin configuration for transactions bot
ADMIN_ID = ADMIN_TELEGRAM_ID = os.getenv('ADMIN_TELEGRAM_ID')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID') 

# Validate bot tokens
def validate_tokens():
    if not TOKEN or TOKEN.startswith('YOUR_BOT_TOKEN'):
        raise ValueError("Please set TELEGRAM_BOT_TOKEN environment variable")
    
    if not ADMIN_TELEGRAM_ID and not ADMIN_CHAT_ID:
        raise ValueError("Please set ADMIN_TELEGRAM_ID or ADMIN_CHAT_ID environment variable")
    
BOT_NAME = os.getenv('BOT_NAME') 

