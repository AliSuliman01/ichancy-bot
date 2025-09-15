from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.howDepositIchancyAccount as message
async def handler(query):
    text , reply_markup = message.how_deposit_ichancy_account_message()
    await query.edit_message_text(text , reply_markup=reply_markup)
