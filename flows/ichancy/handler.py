import Logger
import store
from iChancyAPI import iChancyAPI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import messages.ichancy_message
logger = Logger.getLogger()


async def handler(query , user_id) -> None:
    logger.info(f"User Click on Ichancy Option")
    await query.answer()
    text , reply_markup = messages.ichancy_message.ichancy_message(user_id)
    await query.edit_message_text(text , reply_markup = reply_markup)


