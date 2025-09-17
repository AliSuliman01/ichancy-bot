from telegram.ext import ConversationHandler , MessageHandler , filters , CallbackQueryHandler , ContextTypes ,CommandHandler
from telegram import Update 
import config.telegram
from models.messageToAdmin import MessageToAdmin



async def cancel(update : Update , context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('تم إلغاء عملية ارسال رسالة للأدمن')
    return ConversationHandler.END