
from telegram.ext import filters , CallbackContext , ConversationHandler ,MessageHandler , CallbackQueryHandler ,CommandHandler,ContextTypes
from telegram import ReplyKeyboardRemove, Update 
from models.user import User
from iChancyAPI import iChancyAPI
import config.ichancy
AMMOUNT = 1

async def button_withdrawal_from_account_handler(update:Update , context: CallbackContext):
    await update.callback_query.edit_message_text("ادخل المبلغ المراد سحبه")
    return AMMOUNT