from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.HowWithdrawIchancyAccount as message
async def handler(query):
    await query.edit_message_text(message.how_withdrawal_ichancy_account())
