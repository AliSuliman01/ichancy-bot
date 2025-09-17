from telegram import  Update
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
                "83935571\n"
                "00229271\n\n"
                "اقل قيمة للشحن هي 25,000\n"
                "وأي قيمة أقل من 25,000 لا يمكن شحنها او استرجاعها\n"
                "ثم ادخل رقم عملية التحويل  👇\n"
            )
        )
        return transfeer_NUM

    return ConversationHandler.END