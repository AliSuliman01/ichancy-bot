from telegram.ext import ContextTypes 
from telegram import Update 



MESSAGE = 1
async def button_admin_message_handler(update : Update , context:ContextTypes.DEFAULT_TYPE):
    if update.callback_query.data == 'admin_message':
        await update.callback_query.answer()
        await update.callback_query.message.reply_text("ارسل رسالتك او ارسل صورة هنا") 
    return MESSAGE