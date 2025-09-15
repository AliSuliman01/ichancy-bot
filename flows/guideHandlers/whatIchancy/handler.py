from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.whatIchancy as message
async def handler(query):
    await query.edit_message_text(message.what_ichancy())
