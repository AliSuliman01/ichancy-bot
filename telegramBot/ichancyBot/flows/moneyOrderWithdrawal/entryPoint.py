from telegram import  Update
from messages.money_order_withdrawal_entry_point import money_order_withdrawal_entry_point_message
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )

COMPANY_NAME = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    if query.data == 'order_money_withdrawal':
        text , reply_markup = money_order_withdrawal_entry_point_message()
        await query.edit_message_text(text=text , reply_markup=reply_markup)
        return COMPANY_NAME

    return ConversationHandler.END