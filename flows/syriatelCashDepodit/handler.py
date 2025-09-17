from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.syriatelCashDepodit.entryPoint import button_handler
from flows.syriatelCashDepodit.cancel import cancel
from flows.syriatelCashDepodit.transferNumState import get_transfer_num
from flows.syriatelCashDepodit.valueState import get_value
TRANSFER_NUM ,VALUE = [1,2]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^syriatel_cash_deposit$')],
        states={
            TRANSFER_NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transfer_num)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_value)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler