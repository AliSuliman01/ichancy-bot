from telegram import  Update
from messages.crypto_entry_point import crypto_entry_point_message
import config.crypto
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )

WALLET_TYPE = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'crypto_deposit':
        text , reply_markup = crypto_entry_point_message(DAMUSDT= config.crypto.SYP_for_unit['USDT'] )
        await query.edit_message_text(text=text , reply_markup=reply_markup)
        return WALLET_TYPE

    return ConversationHandler.END