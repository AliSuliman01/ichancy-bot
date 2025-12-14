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
from flows.syriatelCashDepodit.transfeerNumState import get_transfeer_num
from flows.syriatelCashDepodit.valueState import get_value
transfeer_NUM ,VALUE = [1,2]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^syriatel_cash_deposit$')],
        states={
            transfeer_NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transfeer_num)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_value)],
        },
        fallbacks=[CommandHandler('start',start)],
        per_chat=True,
        per_user=True,
        per_message=False,
    )
    return conv_handler