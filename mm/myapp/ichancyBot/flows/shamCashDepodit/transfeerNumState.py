from telegram import  Update
from telegram.ext import CallbackContext

VALUE = 2

async def get_transfer_num(update: Update, context: CallbackContext) -> int:
    transfer_num = update.message.text
    context.user_data["transfer_num"] = transfer_num
    await update.message.reply_text(
        f"ادخل المبلغ الذي تم وصوله إلى الحساب أعلاه"
    )
    return VALUE