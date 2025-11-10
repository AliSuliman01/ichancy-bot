from telegram import  Update
from telegram.ext import CallbackContext , ConversationHandler
import Logger
from flows.moneyOrderWithdrawal.validation.nameValidation import nameValidation
logger = Logger.getLogger()
CITY_NAME = 3

async def get_name(update: Update, context: CallbackContext) -> int:
    name = update.message.text
    if nameValidation(name):
        context.user_data["name"] = name
        await update.message.reply_text(
            f"ادخل اسم المدينة المراد وصول الحوالة لها\n"
        )
    else:
        await update.message.reply_text("يجب ان بتألف الاسم على الأقل من ثلاثة اجزاء ومندون أرقام")
        return ConversationHandler.END
    return CITY_NAME