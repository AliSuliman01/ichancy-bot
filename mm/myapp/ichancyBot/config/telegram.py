from .settings import get_setting

# Bot configuration
TOKEN = get_setting('telegram_bot_token')
TRANSACTIONS_BOT_TOKEN = get_setting('transactions_telegram_bot_token')
# SESSION_FILE = 'ichancy_sessions.json'
COOKIE_STRING = get_setting('ichancy_cookie')
COOKIE_FROM_GROUP_ID = get_setting('cookie_from_group_id')
COOKIE_STATUS = False
UPDATE_COOKIE_DATE:float = 2758801549.062256
COOKIE_MESSAGE_SENT = False
ACTIVE_REFRESHING_COOKIE = False
ACTIVE_REFRESHING_COOKIE_FROM_FILE = False
ACTIVE_REFRESHING_COOKIE_FROM_GROUP = True

# Admin configuration for transactions bot
ADMIN_TELEGRAM_ID = get_setting('admin_telegram_id')
ADMIN_ID = ADMIN_TELEGRAM_ID

ADMIN_CHAT_ID = get_setting('admin_chat_id')

# Validate bot tokens
def validate_tokens():
    if not TOKEN or TOKEN.startswith('YOUR_BOT_TOKEN'):
        raise ValueError("Please set telegram_bot_token in settings table")
    
    if not ADMIN_TELEGRAM_ID and not ADMIN_CHAT_ID:
        raise ValueError("Please set admin_telegram_id or admin_chat_id in settings table")
    
BOT_NAME = get_setting('bot_name')

# Parse comma-separated channel/group IDs
telegram_channels_str = get_setting('telegram_channels')
TELEGRAM_CHANNELS = [ch.strip() for ch in telegram_channels_str.split(',') if ch.strip()] if telegram_channels_str else []

telegram_groups_str = get_setting('telegram_groups')
TELEGRAM_GROUPS = [gr.strip() for gr in telegram_groups_str.split(',') if gr.strip()] if telegram_groups_str else [] 