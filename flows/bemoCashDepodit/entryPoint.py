from telegram import  Update
from config.bemo import BEMO_ACCOUNT , MINIMUM_DEPOSITE
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )

transfeer_NUM = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'bemo_deposit':
        await query.edit_message_text(
            text=(
                "ارسل الى احد الارقام التالية بطريقة التحويل اليدوي\n"
                f"{BEMO_ACCOUNT}\n\n"
                f"اقل قيمة للشحن هي {MINIMUM_DEPOSITE}\n"
                f"وأي قيمة أقل من {MINIMUM_DEPOSITE} لا يمكن شحنها او استرجاعها\n"
                "ثم ادخل رقم عملية التحويل  👇\n"
            )
        )
        return transfeer_NUM

    return ConversationHandler.END