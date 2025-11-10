from telegram import Update ,ReplyKeyboardRemove
from telegram.ext import ConversationHandler ,CallbackContext 


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        'تم إلغاء عملية سحب الرصيد من الكود الهدية',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

