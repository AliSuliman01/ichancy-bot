from telegram import  Update
from telegram.ext import CallbackContext , ConversationHandler
import Logger
from flows.moneyOrderWithdrawal.validation.cityNameValidation import cityNameValidation
logger = Logger.getLogger()
PHONE_NUMBER = 4

async def get_city_name(update: Update, context: CallbackContext) -> int:
    withdraw_city_name = update.message.text
    if cityNameValidation(withdraw_city_name):
        context.user_data["withdraw_city_name"] = withdraw_city_name
        await update.message.reply_text(
            f"ادخل رقم الهاتف الخاص بالمستلم\n"
        )
    else:
        await update.message.reply_text("يرجى إدخال اسم محافظة صحيح")
        return ConversationHandler.END

    return PHONE_NUMBER