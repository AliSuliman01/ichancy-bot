import Logger
import messages.deposit
logger = Logger.getLogger()


async def handler(query , user_id) -> None:
    logger.info(f"User Click on deposite Option")
    await query.answer()
    text , reply_markup = messages.deposit.deposit_message(user_id)
    await query.edit_message_text(text , reply_markup = reply_markup)


