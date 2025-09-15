import Logger
import messages.deposit
logger = Logger.getLogger()


async def handler(query , user_id) -> None:
    logger.info(f"User Click on Withdrawal Option")
    await query.answer()
    await query.edit_message_text(messages.deposit.deposit_message(user_id))


