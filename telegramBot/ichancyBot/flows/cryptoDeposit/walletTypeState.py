from telegram import  Update
from telegram.ext import CallbackContext
import Logger
from config.crypto import wallets , MINIMUM_DEPOSITE
logger = Logger.getLogger()
TRANSFEER_NUM = 2

async def get_wallet_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    wallet_type = query.data
    context.user_data["wallet_type"] = wallet_type
    await query.edit_message_text(
                "ارسل المبلغ المراد تحويله الى المحفظة التالية\n"
                f"{wallets[wallet_type]}\n\n"
                f"اقل قيمة للشحن هي {MINIMUM_DEPOSITE} $ \n"
                f"وأي قيمة أقل من {MINIMUM_DEPOSITE} لا يمكن شحنها او استرجاعها\n"
                "ثم ادخل رقم عملية التحويل  👇\n"
            )
    return TRANSFEER_NUM