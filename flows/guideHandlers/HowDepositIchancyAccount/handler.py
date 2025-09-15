from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.howDepositIchancyAccount as message
async def handler(query):
    await query.edit_message_text(message.how_deposit_ichancy_account_message())
