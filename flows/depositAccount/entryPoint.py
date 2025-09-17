from telegram import Update  
from telegram.ext import  ContextTypes
AMMOUNT = 1

async def button_deposit_account_handler(update : Update , context : ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("ادخل المبلغ المراد تحويله")
    return AMMOUNT
