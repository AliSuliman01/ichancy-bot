from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.guides_message as message

async def handler(query):
    
    await query.edit_message_text(message.guides_message())
