from telegram import Update 
from telegram.ext import CallbackContext
CODE = 1

async def button_reseive_gift_handler(update: Update , context:CallbackContext ):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("يرجى إدخال الكود المخصص للهدية")
    return CODE