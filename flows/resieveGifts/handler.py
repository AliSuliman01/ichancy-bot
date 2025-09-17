
from telegram.ext import ConversationHandler , CallbackQueryHandler ,MessageHandler ,filters ,CommandHandler
from flows.resieveGifts.cancel import cancel
from flows.resieveGifts.entryPoint import button_reseive_gift_handler
from flows.resieveGifts.codeState import get_code
CODE = 1

def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points= [CallbackQueryHandler(button_reseive_gift_handler , pattern='^reseive_gift$')],
        states={
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND , get_code)]
        },
     fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler