from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.howToCreateNewAccount as message
async def handler(query):
    text , reply_markup = message.how_to_create_new_account()
    await query.edit_message_text(text , reply_markup = reply_markup)
