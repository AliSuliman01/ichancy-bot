from telegram import  Update
from telegram.ext import CallbackContext
import Logger
from config.syriatel import MINIMUM_WITHDRAW
logger = Logger.getLogger()
VALUE = 2

async def get_withdraw_number(update: Update, context: CallbackContext) -> int:
    withdraw_number = update.message.text
    context.user_data["withdraw_number"] = withdraw_number
    await update.message.reply_text(
        f"ادخل المبلغ الذي تريد سحبه\n"
        f"إن أقل قيمة للسحب هي {MINIMUM_WITHDRAW}"
    )
    return VALUE