from telegram import  Update
from config.shamCash import SHAM_CASH_ACCOUNT
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )

transfeer_NUM = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'sham_cash_deposit':
        await query.edit_message_text(
            text=(
                "ارسل الى العنوان التالي  \n"
                f"{SHAM_CASH_ACCOUNT}\n\n"
                "ثم ادخل رقم عملية التحويل  👇\n"
            )
        )
        return transfeer_NUM

    return ConversationHandler.END