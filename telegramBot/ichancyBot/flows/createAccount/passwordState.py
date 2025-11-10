import asyncio
import Logger 
from telegram import Update
from telegram.ext import (ConversationHandler,CallbackContext)
import flows.createAccount.handler as handling
logger = Logger.getLogger()


async def get_password(update: Update, context: CallbackContext) -> int:

    # if not config.telegram.COOKIE_STATUS:
    #     await update.message.reply_text("عملية صيانة دورية للبوت وسيتم إعادة تشغيله خلال بضع دقائق")
    #     return ConversationHandler.END
    await update.message.reply_text("المعالجة جارية")
    task = asyncio.create_task(handling.finishingHandler(update , context))
    if 'background_tasks' not in context.application.bot_data:
        context.application.bot_data['background_tasks'] = set()
    context.application.bot_data['background_tasks'].add(task)
    task.add_done_callback(lambda t: context.application.bot_data['background_tasks'].discard(t))
    return ConversationHandler.END
   
   