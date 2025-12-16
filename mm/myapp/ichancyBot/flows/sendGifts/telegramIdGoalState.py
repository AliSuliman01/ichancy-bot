from telegram import Update 
from telegram.ext import CallbackContext
import Logger
import string
import Logger
from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
import Logger
logger = Logger.getLogger()
ammount = 2
async def get_telegram_id_goal(update: Update, context: CallbackContext) -> int:
    telegramIdGoal = update.message.text 
    context.user_data['telegramIdGoal'] = telegramIdGoal
    await update.message.reply_text(
        f"أدخل الكمية المراد إهداؤها"
    )
    return ammount

