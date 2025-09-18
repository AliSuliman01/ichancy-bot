from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.bemoCashDepodit.entryPoint import button_handler
from flows.bemoCashDepodit.cancel import cancel
from flows.bemoCashDepodit.transfeerNumState import get_transfeer_num
from flows.bemoCashDepodit.valueState import get_value
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