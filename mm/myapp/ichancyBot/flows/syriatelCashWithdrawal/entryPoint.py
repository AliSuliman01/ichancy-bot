from telegram import  Update
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )

WITHDRAW_NUMBER = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'syriatel_cash_withdraw':
        await query.edit_message_text("أرسل رقم سيريتيل الذي ترغب في استقبال ارباحك عليه")
        return WITHDRAW_NUMBER

    return ConversationHandler.END