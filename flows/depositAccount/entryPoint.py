from telegram import Update  
from telegram.ext import  ContextTypes , ConversationHandler
import config.telegram
AMMOUNT = 1

async def button_deposit_account_handler(update : Update , context : ContextTypes.DEFAULT_TYPE):
    # if not config.telegram.COOKIE_STATUS:
    #     await update.message.reply_text("عملية صيانة دورية للبوت وسيتم إعادة تشغيله خلال بضع دقائق")
    #     return ConversationHandler.END
    
    await update.callback_query.edit_message_text("ادخل المبلغ المراد تحويله")
    return AMMOUNT
