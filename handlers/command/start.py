import Logger
from telegram import Update
from telegram.ext import (
    ContextTypes
)
import store
import helpers
logger = Logger.getLogger()




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id , username =  await helpers.getInfo(update , context)
    store.insertNewUser(user_id , username)
    await update.message.reply_text(helpers.getTextWelcome(username), 
                                    reply_markup=helpers.getReplyMarkup(), 
                                    parse_mode='Markdown')
