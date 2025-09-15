from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.guides_message as message

async def handler(query):
    text , reply_markup = message.guides_message(query)
    await query.edit_message_text(text , reply_markup = reply_markup)
