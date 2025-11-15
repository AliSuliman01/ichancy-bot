import Logger
import config.telegram
from cryptoPrices import CryptoPrices

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
    print(update.message.chat.id)
    if int(newCookieId) - int(config.telegram.COOKIE_FROM_GROUP_ID) == 0 and update.message.text.find('PHPSESSID') !=-1 and config.telegram.ACTIVE_REFRESHING_COOKIE_FROM_GROUP:
        newCookieString = update.message.text
        config.telegram.COOKIE_STRING = newCookieString
        config.telegram.COOKIE_STATUS = True
        print(config.telegram.COOKIE_STRING)

async def sendCookieNotification(context:CallbackContext):
    
    if not config.telegram.COOKIE_STATUS and not config.telegram.COOKIE_MESSAGE_SENT:
        await context.bot.send_message(
            chat_id=config.telegram.COOKIE_FROM_GROUP_ID,
            text="NEED COOKIE")
def main() -> None:

    try:
        application = Application.builder().token(config.telegram.TOKEN).build()
        if config.telegram.ACTIVE_REFRESHING_COOKIE_FROM_GROUP:
            job_queue = application.job_queue
            job_queue.run_repeating(
            sendCookieNotification,
            interval=10, 
            first=5      
            )

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
        application.add_handler(flows.cryptoDeposit.handler.conversationHandler())
        application.add_handler(CallbackQueryHandler(button.button))
        application.add_error_handler(flows.error.handler.error_handler)
        application.add_handler(MessageHandler(filters.TEXT  & ~filters.COMMAND , cookieHandler))
      

        logger.info("Starting iChancy Account Manager Bot...")
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        application.run_polling(
            poll_interval=1.0,
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
         referal = referalThread()
         referal.start()
         cryptoPrices = CryptoPrices()
         cryptoPrices.start()
         if config.telegram.ACTIVE_REFRESHING_COOKIE:
             refreshingCookie = RefreshingCookieThread()
             refreshingCookie.start()
         if config.telegram.ACTIVE_REFRESHING_COOKIE_FROM_FILE:
             refreshingCookieFromFile = RefreshingCookieFromFileThread()
             refreshingCookieFromFile.start()
         main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)


