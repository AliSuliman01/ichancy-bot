from telegram import  Update
from telegram.ext import CallbackContext
import Logger
from models.syriatelTransaction import SyriatelTransaction
from models.user import User
logger = Logger.getLogger()
VALUE = 2

async def get_transfeer_num(update: Update, context: CallbackContext) -> int:
    transfeer_num = update.message.text
    context.user_data["transfeer_num"] = transfeer_num
    await update.message.reply_text(
        f"ادخل المبلغ الذي تم وصوله إلى الأرقام أعلاه"
    )
    return VALUE