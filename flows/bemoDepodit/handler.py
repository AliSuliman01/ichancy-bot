from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.bemoDepodit.entryPoint import button_handler
from flows.bemoDepodit.cancel import cancel
from flows.bemoDepodit.transfeerNumState import get_transfeer_num
from flows.bemoDepodit.valueState import get_value
transfeer_NUM ,VALUE = [1,2]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^bemo_deposit$')],
        states={
            transfeer_NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transfeer_num)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_value)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler