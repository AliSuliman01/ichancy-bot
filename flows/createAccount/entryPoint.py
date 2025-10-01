from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import (ContextTypes,ConversationHandler,CallbackContext,MessageHandler,filters,CommandHandler,CallbackQueryHandler)
import config.telegram
USERNAME = 1


async def button_handler(update: Update, context: CallbackContext) -> int:
    # if not config.telegram.COOKIE_STATUS:
    #     await update.callback_query.edit_message_text("عملية صيانة دورية للبوت وسيتم إعادة تشغيله خلال بضع دقائق")
    #     return ConversationHandler.END
    query = update.callback_query
    await query.answer()

    if query.data == 'create_account':
        await query.edit_message_text(
            text="ادخل اسم المستخدم" ,parse_mode='Markdown'
        )
        return USERNAME

    return ConversationHandler.END