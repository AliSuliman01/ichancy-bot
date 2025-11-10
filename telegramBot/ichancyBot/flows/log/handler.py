import Logger
from messages.log import log_message
logger = Logger.getLogger()

async def handler(query):
    logger.info("from log handler")
    text_welcome , reply_markup = log_message()
    logger.info("passed get log message successfully")
    await query.edit_message_text(
        text_welcome,
        reply_markup=reply_markup,
    )