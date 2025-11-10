from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.HowWithdrawIchancyAccount as message
async def handler(query):
    text , reply_markup = message.how_withdrawal_ichancy_account()
    await query.edit_message_text(text , reply_markup = reply_markup)
