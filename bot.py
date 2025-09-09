import Logger
import config.telegram
import handlers.createAccount , handlers.error , handlers.button , handlers.syriatel_cash_deposit
import handlers.command.start , handlers.command.balance
from iChancyAPI import iChancyAPI
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler
)
logger = Logger.getLogger()

if not config.telegram.TOKEN or config.telegram.TOKEN.startswith('YOUR_BOT_TOKEN'):
    logger.error("Please set TELEGRAM_BOT_TOKEN environment variable")
    exit(1)


def main() -> None:
    """Main function to start the bot"""
    try:
        # Set cookies from the provided cookie string
        
        iChancyAPI.set_cookies_from_string(config.telegram.COOKIE_STRING)
        
        # Create application
        application = Application.builder().token(config.telegram.TOKEN).build()
        # Add conversations

        # Add handlers
        application.add_handler(handlers.createAccount.conversationHandler())
        application.add_handler(handlers.syriatel_cash_deposit.conversationHandler())
        application.add_handler(CommandHandler('start', handlers.command.start.start))
        application.add_handler(CommandHandler('balance', handlers.command.balance))
        # application.add_handler(CallbackQueryHandler(ichancy))
        application.add_handler(CallbackQueryHandler(handlers.button.button))
        application.add_error_handler(handlers.error.error_handler)

        # Start the bot
        logger.info("Starting iChancy Account Manager Bot...")
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        application.run_polling(
            poll_interval=2.0,
            timeout=30,
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
    finally:
        logger.info("Bot shutdown complete")

if __name__ == '__main__':
    import sys
    
    logger.info("Initializing iChancy Account Manager Bot...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
