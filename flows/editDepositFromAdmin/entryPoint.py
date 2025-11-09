from telegram import  Update
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )
from config.telegram import ADMIN_ID
EDIT = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    chat_id = context.user_data["chat_id"] = query.data.split(" ")[4]
    await query.answer()
    if query.data.split(" ")[0] == 'edit_deposit':
        await context.bot.send_message(chat_id = chat_id ,
            text="يرجى إدخال القيمة الجديدة   "
        )
        currency = query.data.split(" ")[2] 
        realValue = query.data.split(" ")[3]
        context.user_data["currency"] = currency
        context.user_data["realValue"] = realValue
        context.user_data["transaction_id"] = query.data.split(" ")[1]
        context.user_data["message"] = update.callback_query.message.text
        context.user_data["message_id"] = update.callback_query.message.message_id
        context.user_data["reply_markup"] = update.callback_query.message.reply_markup
        return EDIT

    return ConversationHandler.END

