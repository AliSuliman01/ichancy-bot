from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.whatIchancy as message
async def handler(query):
    text , reply_markup = message.what_ichancy()
    await query.edit_message_text(text , reply_markup = reply_markup)
