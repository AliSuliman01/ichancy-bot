from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
import messages.guideMessages.HowWithdrawTelegramAccount as message
async def handler(query):
    text , reply_markup = message.how_withdrawal_telegram_account()
    await query.edit_message_text(text , reply_markup = reply_markup)
