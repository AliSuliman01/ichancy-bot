from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.syriatelCashDepodit.entryPoint import button_handler
from flows.syriatelCashDepodit.cancel import cancel
from flows.startFlow.handler import start
from flows.syriatelCashDepodit.transfeerNumState import get_transfer_num
from flows.syriatelCashDepodit.valueState import get_value
transfer_num ,VALUE = [1,2]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^syriatel_cash_deposit$')],
        states={
            transfer_num: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transfer_num)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_value)],
        },
        fallbacks=[CommandHandler('start',start)],
        per_chat=True,
        per_user=True,
        per_message=False,
    )
    return conv_handler