


def getHelpText():
        help_text = (
        "❓ **Help & Information**\n\n"
        "🤖 **Bot Commands:**\n"
        "• `/start` - Start the bot and show main menu\n\n"
        "🔧 **Features:**\n"
        "• Create new iChancy accounts automatically\n"
        "• Check account status\n"
        "• Account management (saves your account info)\n\n"
        "⚠️ **Important Notes:**\n"
        "• This bot is for educational purposes\n"
        "• Respect iChancy's terms of service\n"
        "• Keep your credentials secure\n\n"
        "🔧 **How it works:**\n"
        "1. Click 'Create New Account'\n"
        "2. Bot generates random credentials\n"
        "3. Submits registration to iChancy\n"
        "4. Saves account info for you"
    )
        return help_text

def getStatusText(user , created_time):
    status_text = (
        "https://www.ichancy.com/ar \n\n"
        f"👤 الدخول: {user['name']}\n"
        f"📧 الإيميل: {user['email']}\n"
        f"🔒 كلمة السر: {user['password']} "
    )
    return status_text