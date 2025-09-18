from telegram import  Update
from config.syriatel import SYRIATEL_ACCOUNT ,MINIMUM_DEPOSITE
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )

transfeer_NUM = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'syriatel_cash_deposit':
        await query.edit_message_text(
            text=(
                "ارسل الى احد الارقام التالية بطريقة التحويل اليدوي\n"
                f"{SYRIATEL_ACCOUNT}\n\n"
                f"اقل قيمة للشحن هي {MINIMUM_DEPOSITE}\n"
                f"وأي قيمة أقل من {MINIMUM_DEPOSITE} لا يمكن شحنها او استرجاعها\n"
                "ثم ادخل رقم عملية التحويل  👇\n"
            )
        )
        return transfeer_NUM

    return ConversationHandler.END