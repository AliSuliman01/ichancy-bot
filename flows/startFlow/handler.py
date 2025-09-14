from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from messages import start_message
from models.user import User

def handler():  
    return CommandHandler('start', start)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or update.effective_user.first_name
    User().insert({
        'telegram_id': user_id,
        'username': username
    })
    
    reply_text, reply_markup = start_message()

    await update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode='Markdown')
