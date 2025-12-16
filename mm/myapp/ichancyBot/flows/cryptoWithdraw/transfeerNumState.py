from telegram import  Update
from telegram.ext import CallbackContext
import Logger
logger = Logger.getLogger()
VALUE = 3

async def get_transfer_num(update: Update, context: CallbackContext) -> int:
    transfer_num = update.message.text
    context.user_data["transfer_num"] = transfer_num
    
    await update.message.reply_text('ادخل المبلغ الذي تريد سحبه من عملة USDT')
    
    return VALUE