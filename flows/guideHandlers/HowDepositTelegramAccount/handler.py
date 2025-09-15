from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.howDepositTelegramAccount as message
async def handler(query):
    await query.edit_message_text(message.how_deposit_telegram_account_message())
