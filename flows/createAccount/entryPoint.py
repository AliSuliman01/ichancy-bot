from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import (ContextTypes,ConversationHandler,CallbackContext,MessageHandler,filters,CommandHandler,CallbackQueryHandler)

USERNAME = 1


async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'create_account':
        await query.edit_message_text(
            text="ادخل اسم المستخدم" ,parse_mode='Markdown'
        )
        return USERNAME

    return ConversationHandler.END