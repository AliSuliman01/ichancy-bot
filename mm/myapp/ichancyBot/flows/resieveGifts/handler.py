
from telegram.ext import ConversationHandler , CallbackQueryHandler ,MessageHandler ,filters ,CommandHandler
from flows.resieveGifts.cancel import cancel
from flows.startFlow.handler import start
from flows.resieveGifts.entryPoint import button_reseive_gift_handler
from flows.resieveGifts.codeState import get_code
CODE = 1

def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points= [CallbackQueryHandler(button_reseive_gift_handler , pattern='^reseive_gift$')],
        states={
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND , get_code)]
        },
     fallbacks=[CommandHandler('start',start)],
     per_chat=True,
     per_user=True,
     per_message=False,
    )
    return conv_handler