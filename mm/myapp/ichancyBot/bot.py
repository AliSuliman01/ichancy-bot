import os
import Logger
import config.telegram
from cryptoPrices import CryptoPrices
import warnings
from telegram.warnings import PTBUserWarning
import asyncio

# Suppress PTBUserWarning about per_message=False with CallbackQueryHandler
# This is expected behavior when using mixed handlers (CallbackQueryHandler + MessageHandler)
warnings.filterwarnings("ignore", category=PTBUserWarning, message=".*per_message=False.*CallbackQueryHandler.*")
# Suppress PTBUserWarning about JobQueue not being set up
warnings.filterwarnings("ignore", category=PTBUserWarning, message=".*JobQueue.*")

import  button
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext
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
import flows.bemoWithdrawal.handler
import flows.editDepositFromAdmin.handler
import flows.editWithdrawFromAdmin.handler
import flows.shamCashDepodit.handler
import flows.syriatelCashWithdrawal.handler
import flows.shamCashWithdrawal.handler
import flows.moneyOrderWithdrawal.handler
import flows.cryptoDeposit.handler
import flows.cryptoWithdraw.handler
import flows.backToMenu.handler 
from referalHandler import referalThread
from refreshingCookie import RefreshingCookieThread
from refreshingCookieFromFile import RefreshingCookieFromFileThread
from threadManager import get_thread_manager
logger = Logger.getLogger()

try:
    config.telegram.validate_tokens()
except ValueError as e:
    logger.error(str(e))
    exit(1)
############################for animation##############################
# async def cookieHandler(update:Update , context: ContextTypes.DEFAULT_TYPE):
#     newCookieId = int(update.message.from_user.id)
#     print(update.message)
#     if newCookieId - int(config.telegram.ADMIN_ID)== 0 and update.message.text.find('PHPSESSID') !=-1:
#         newCookieString = update.message.text.split("\n")[0].replace("ع","_")
#         config.telegram.COOKIE_STRING = newCookieString
#         config.telegram.UPDATE_COOKIE_DATE = float(update.message.text.split("\n")[1])
#         logger.info(f"OUR NEW COOKIE IS {config.telegram.COOKIE_STRING}")
#         logger.info(f"the date the cookie become new is : {config.telegram.UPDATE_COOKIE_DATE}")
#         config.telegram.COOKIE_STATUS = True
#     if newCookieId - int(config.telegram.ADMIN_ID)== 0 and update.message.text.find('OK') !=-1:
#         config.telegram.COOKIE_MESSAGE_SENT = True
#############################################################################
async def cookieHandler(update:Update , context: ContextTypes.DEFAULT_TYPE):
    newCookieId = int(update.message.chat.id)
    # print(update.message.chat.id)
    if int(newCookieId) - int(config.telegram.COOKIE_FROM_GROUP_ID) == 0 and update.message.text.find('PHPSESSID') !=-1 and config.telegram.ACTIVE_REFRESHING_COOKIE_FROM_GROUP:
        newCookieString = update.message.text
        config.telegram.COOKIE_STRING = newCookieString
        config.telegram.COOKIE_STATUS = True
        # print(config.telegram.COOKIE_STRING)
        # Reply with success confirmation
        await update.message.reply_text("✅ Cookie updated successfully!")

async def sendCookieNotification(context:CallbackContext):
    
    if not config.telegram.COOKIE_STATUS and not config.telegram.COOKIE_MESSAGE_SENT:
        # logger.info(f"sending NEED COOKIE to group: {config.telegram.COOKIE_FROM_GROUP_ID}")
        await context.bot.send_message(
            chat_id=config.telegram.COOKIE_FROM_GROUP_ID,
            text="NEED COOKIE")

def _run_bot_with_initialization(application):
    """Helper function to run bot with proper async initialization"""
    async def _async_run():
        async with application:
            await application.updater.start_polling(
                poll_interval=1.0,
                timeout=30,
                drop_pending_updates=True
            )
            # Keep running until interrupted
            await asyncio.Event().wait()
    
    asyncio.run(_async_run())

def main() -> None:

    try:
        application = Application.builder().token(config.telegram.TOKEN).build()
        if config.telegram.ACTIVE_REFRESHING_COOKIE_FROM_GROUP:
            job_queue = application.job_queue
            if job_queue is not None:
                job_queue.run_repeating(
                    sendCookieNotification,
                    interval=60, 
                    first=5      
                )
            else:
                # JobQueue not available - cookie notification will not be sent automatically
                # This is handled gracefully, no need to log warning as it's already suppressed
                pass

        application.add_handler(flows.createAccount.handler.conversationHandler())
        application.add_handler(flows.syriatelCashDepodit.handler.conversationHandler())
        application.add_handler(flows.syriatelCashWithdrawal.handler.conversationHandler())
        application.add_handler(flows.bemoDepodit.handler.conversationHandler())
        application.add_handler(flows.bemoWithdrawal.handler.conversationHandler())
        application.add_handler(flows.shamCashDepodit.handler.conversationHandler())
        application.add_handler(flows.shamCashWithdrawal.handler.conversationHandler())
        application.add_handler(flows.sendGifts.handler.conversationHandler())
        application.add_handler(flows.resieveGifts.handler.conversationHandler())
        application.add_handler(flows.depositAccount.handler.conversationHandler())
        application.add_handler(flows.withdrawalAccount.handler.conversationHandler())
        application.add_handler(flows.editDepositFromAdmin.handler.conversationHandler())
        application.add_handler(flows.editWithdrawFromAdmin.handler.conversationHandler())
        application.add_handler(flows.moneyOrderWithdrawal.handler.conversationHandler())
        application.add_handler(flows.cryptoDeposit.handler.conversationHandler())
        application.add_handler(flows.cryptoWithdraw.handler.conversationHandler())
        application.add_handler(flows.messageToAdmin.handler.handler())
        application.add_handler(flows.startFlow.handler.handler())
        application.add_handler(flows.balanceCommand.handler.handler())
        application.add_handler(CallbackQueryHandler(button.button))
        application.add_error_handler(flows.error.handler.error_handler)
        application.add_handler(MessageHandler(filters.TEXT  & ~filters.COMMAND , cookieHandler))
      

        # logger.info("Starting iChancy Account Manager Bot...")
        # logger.info("Bot is running. Press Ctrl+C to stop.")
        
        # Use helper function to ensure proper async initialization
        # _run_bot_with_initialization(application)

        
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
        logger.info("Bot application shutdown complete")

if __name__ == '__main__':
    import sys
    import signal
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        sys.exit(1)
    
    # Get thread manager instance
    thread_manager = get_thread_manager()
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        # logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        thread_manager.stop_all()
        sys.exit(0)
    
    # Register signal handlers (SIGTERM not available on Windows)
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Create and register threads
        referal = referalThread()
        thread_manager.register_thread(referal, "ReferralThread")
        
        # CryptoPrices thread - can be disabled by setting environment variable
        # if os.environ.get('DISABLE_CRYPTO_PRICES', '').lower() not in ('1', 'true', 'yes'):
        #     cryptoPrices = CryptoPrices()
        #     thread_manager.register_thread(cryptoPrices, "CryptoPrices")
        
        if config.telegram.ACTIVE_REFRESHING_COOKIE:
            refreshingCookie = RefreshingCookieThread()
            thread_manager.register_thread(refreshingCookie, "RefreshingCookieThread")
        elif config.telegram.ACTIVE_REFRESHING_COOKIE_FROM_FILE:
            refreshingCookieFromFile = RefreshingCookieFromFileThread()
            thread_manager.register_thread(refreshingCookieFromFile, "RefreshingCookieFromFileThread")
        
        # Start all threads
        thread_manager.start_all()
        
        # Run main bot (run_polling handles async internally)
        main()
        
    # except KeyboardInterrupt:
        # logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
    finally:
        # Ensure all threads are stopped
        # logger.info("Shutting down all background threads...")
        thread_manager.stop_all()
        # logger.info("Bot shutdown complete")


