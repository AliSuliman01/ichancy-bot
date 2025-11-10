from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.howDepositTelegramAccount as message
async def handler(query):
    text , reply_markup = message.how_deposit_telegram_account_message()
    await query.edit_message_text(text , reply_markup = reply_markup)
