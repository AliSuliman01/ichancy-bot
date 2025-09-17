import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from messages.start_message import start_message
logger = Logger.getLogger()

async def handler(query , username):
    """Return to main menu"""
    text_welcome , reply_markup = start_message()
    await query.edit_message_text(
        text_welcome,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )