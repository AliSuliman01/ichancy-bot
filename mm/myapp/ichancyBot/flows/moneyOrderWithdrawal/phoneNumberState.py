from telegram import  Update
from telegram.ext import CallbackContext ,ConversationHandler
import Logger
from config.orderMoney import MINIMUM_WITHDRAW
from flows.moneyOrderWithdrawal.validation.phoneValidation import phoneValidation
logger = Logger.getLogger()
VALUE = 5

async def get_phone_number(update: Update, context: CallbackContext) -> int:
    phone_number = update.message.text
    if phoneValidation(phone_number):
        text = f"أدخل المبلغ المراد سحبه\n أقل قيكة للسحب هي {MINIMUM_WITHDRAW}"
        context.user_data["phone_number"] = phone_number
        await update.message.reply_text(text)
    else:
         text  = "يجب ان يتكون رقم الهاتف من عشرة ارقام"
         await update.message.reply_text(text)
         return ConversationHandler.END
   
    return VALUE