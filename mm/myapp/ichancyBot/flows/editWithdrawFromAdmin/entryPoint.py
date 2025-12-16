from telegram import  Update
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )
from config.telegram import ADMIN_ID
EDIT = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    chat_id = context.user_data["chat_id"] = query.data.split(" ")[3]
    await query.answer()
    if query.data.split(" ")[0] == 'edit_withdraw':
        await context.bot.send_message(chat_id = chat_id ,
            text="يرجى إدخال القيمة الجديدة   "
        )
        
        context.user_data["transaction_id"] = query.data.split(" ")[1]
        # print("#"*100)
        # print(query.data.split(" ")[1])
        # print("#"*100)
        context.user_data["TAX"] = float(query.data.split(" ")[2])
        context.user_data["message"] = update.callback_query.message.text
        context.user_data["message_id"] = update.callback_query.message.message_id
        context.user_data["reply_markup"] = update.callback_query.message.reply_markup
        return EDIT

    return ConversationHandler.END

