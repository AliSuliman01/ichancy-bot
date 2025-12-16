from telegram import  Update
from config.bemo import BEMO_ACCOUNT , MINIMUM_DEPOSITE
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )

transfer_num = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'bemo_deposit':
        await query.edit_message_text(
            text=(
                "ارسل الى الحساب التالي\n"
                f"{BEMO_ACCOUNT}\n\n"
                f"اقل قيمة للشحن هي {MINIMUM_DEPOSITE}\n"
                f"وأي قيمة أقل من {MINIMUM_DEPOSITE} لا يمكن شحنها او استرجاعها\n"
                "ثم ادخل رقم عملية التحويل  👇\n"
            )
        )
        return transfer_num

    return ConversationHandler.END