import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from messages.start_message import start_message
logger = Logger.getLogger()

async def handler(update , context , query = None):
    """Return to main menu"""
###################################################
    #cus we have a callback query that have backToMenu and Doesnt end the ConversationHandler
    if query == None :
        query = update.callback_query
    if query.from_user.id:
        context.application.drop_user_data(query.from_user.id)
###################################################
    text_welcome , reply_markup = start_message()
    await query.edit_message_text(
        text_welcome,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    #cus we have a callback query that have backToMenu and Doesnt end the ConversationHandler
    return ConversationHandler.END