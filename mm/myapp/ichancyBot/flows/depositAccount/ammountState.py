from telegram import Update  
from iChancyAPI import iChancyAPI
from telegram.ext import ConversationHandler , ContextTypes
import config.ichancy ,config.telegram
from models.user import User
from models.accountTransaction import AccountTransaction
from flows.depositAccount.validations import balanceSuficient , adminBalanceSuficient , isDigit
import flows.depositAccount.handler
import asyncio
async def get_ammount_for_deposit(update: Update , context : ContextTypes.DEFAULT_TYPE):
    # if not config.telegram.COOKIE_STATUS:
    #     await update.message.reply_text("عملية صيانة دورية للبوت وسيتم إعادة تشغيله خلال بضع دقائق")
    #     return ConversationHandler.END
    await update.message.reply_text("المعالجة جارية")
    task = asyncio.create_task(flows.depositAccount.handler.finishungHandling(update , context))
    if 'background_tasks' not in context.application.bot_data:
        context.application.bot_data['background_tasks'] = set()
    context.application.bot_data['background_tasks'].add(task)
    task.add_done_callback(lambda t: context.application.bot_data['background_tasks'].discard(t))
    return ConversationHandler.END
  

