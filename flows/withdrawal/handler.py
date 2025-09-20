import Logger
import messages.withdrawal
logger = Logger.getLogger()


async def handler(query) -> None:
    logger.info(f"User Click on Withdrawal Option")
    await query.answer()
    text , reply_markup = messages.withdrawal.withdrawal_message()
    await query.edit_message_text(text , reply_markup = reply_markup)



# ارسل رقم السيرياتيل الذي ترغب في استقبال ارباحك عليه
# 