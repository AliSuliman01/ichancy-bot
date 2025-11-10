from telegram.ext import filters , CallbackContext , ConversationHandler ,MessageHandler , CallbackQueryHandler ,CommandHandler,ContextTypes
from telegram import ReplyKeyboardRemove, Update 

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "تم إالغاء عملية الإيداع",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END