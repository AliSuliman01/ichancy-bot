import store
from telegram import Update
from telegram.ext import ContextTypes , CommandHandler
import messages.balanceCommadIfUserNotExists
import messages.balanceCommandIfUserExists
from models.user import User

def handler():  
    return CommandHandler('balance', balance)


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Balance command handler"""
    telegram_id = str(update.effective_user.id)
    user = User().getBy({'telegram_id': ('=' , telegram_id)})
    if not user:
        text , reply_markup = messages.balanceCommadIfUserNotExists.message()
        await update.message.reply_text(text=text , reply_markup= reply_markup)
        return
    user = user[0]
    balance = user.get('balance')
    text , reply_markup = messages.balanceCommandIfUserExists.message(balance , telegram_id)
    await update.message.reply_text(text = text , reply_markup=reply_markup)
