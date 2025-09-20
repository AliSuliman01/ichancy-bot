import Logger
import config.telegram
import  button
from telegram.ext import (
    Application,
    CallbackQueryHandler,
)
import flows.startFlow.handler
import flows.messageToAdmin.handler
import flows.withdrawalAccount.handler
import flows.resieveGifts.handler
import flows.sendGifts.handler
import flows.depositAccount.handler
import flows.balanceCommand.handler
import flows.error.handler
import flows.createAccount.handler
import flows.syriatelCashDepodit.handler
import flows.bemoDepodit.handler
import flows.editDepositFromAdmin.handler
import flows.editWithdrawFromAdmin.handler
import flows.shamCashDepodit.handler
import flows.syriatelCashWithdrawal.handler
logger = Logger.getLogger()

try:
    config.telegram.validate_tokens()
except ValueError as e:
    logger.error(str(e))
    exit(1)


def main() -> None:
    """Main function to start the bot"""
    try:
                
        # Create application
        application = Application.builder().token(config.telegram.TOKEN).build()
        # Add conversations

        # Add handlers
        application.add_handler(flows.createAccount.handler.conversationHandler())
        application.add_handler(flows.syriatelCashDepodit.handler.conversationHandler())
        application.add_handler(flows.syriatelCashWithdrawal.handler.conversationHandler())
        application.add_handler(flows.bemoDepodit.handler.conversationHandler())
        application.add_handler(flows.shamCashDepodit.handler.conversationHandler())
        application.add_handler(flows.sendGifts.handler.conversationHandler())
        application.add_handler(flows.resieveGifts.handler.conversationHandler())
        application.add_handler(flows.depositAccount.handler.conversationHandler())
        application.add_handler(flows.withdrawalAccount.handler.conversationHandler())
        application.add_handler(flows.editDepositFromAdmin.handler.conversationHandler())
        application.add_handler(flows.editWithdrawFromAdmin.handler.conversationHandler())
        application.add_handler(flows.messageToAdmin.handler.handler())
        application.add_handler(flows.startFlow.handler.handler())
        application.add_handler(flows.balanceCommand.handler.handler())
        # application.add_handler(CallbackQueryHandler(ichancy))
        application.add_handler(CallbackQueryHandler(button.button))
        application.add_error_handler(flows.error.handler.error_handler)

        # application.add_handler(CallbackQueryHandler(handlers.transactions_handlers.handle_transaction_callback))
        # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.transactions_handlers.handle_message))
        
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
