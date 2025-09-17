import Logger 
from telegram import Update
from telegram.ext import (ContextTypes,ConversationHandler,MessageHandler,filters,CommandHandler,CallbackQueryHandler)
from flows.createAccount.cancel import cancel
from flows.createAccount.entryPoint import button_handler
from flows.createAccount.passwordState import get_password
from flows.createAccount.userNameState import get_username
logger = Logger.getLogger()

USERNAME, PASSWORD = [1,2]

def conversationHandler():
    conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern='^create_account$')],
    states={
        USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
        PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )    
    return conv_handler