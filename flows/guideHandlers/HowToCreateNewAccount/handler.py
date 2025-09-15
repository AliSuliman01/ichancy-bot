from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.howToCreateNewAccount as message
async def handler(query):
    await query.edit_message_text(message.how_to_create_new_account())
