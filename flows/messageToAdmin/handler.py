from telegram.ext import ConversationHandler , MessageHandler , filters , CallbackQueryHandler ,CommandHandler
from flows.messageToAdmin.cancel import cancel
from flows.messageToAdmin.entryPoint import button_admin_message_handler
from flows.messageToAdmin.messageState import get_message
MESSAGE = 1


def handler():
    
    conv_handeler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_admin_message_handler,pattern='^admin_message$')] ,
        states={
            MESSAGE :[MessageHandler(filters.PHOTO |filters.TEXT & ~filters.COMMAND, get_message)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        
    )


    return conv_handeler