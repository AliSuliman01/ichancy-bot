from telegram import  Update,ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        'تم إلغاء عملية السحب.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END