from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.HowWithdrawTelegramAccount as message
async def handler(query):
    await query.edit_message_text(message.how_withdrawal_telegram_account())
