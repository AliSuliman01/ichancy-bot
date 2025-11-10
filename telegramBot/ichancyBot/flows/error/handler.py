import Logger
from telegram import  Update
from telegram.ext import (
    ContextTypes,
)

logger = Logger.getLogger()

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    try:
        if update and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ **An error occurred**\n\nPlease try again later or contact support.",
                parse_mode='Markdown'
            )
    except Exception:
        logger.error("Failed to send error message to user")
