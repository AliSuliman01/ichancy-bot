from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.syriatelCashWithdrawal.entryPoint import button_handler
from flows.syriatelCashWithdrawal.cancel import cancel
from flows.syriatelCashWithdrawal.withdrawNumberState import get_withdraw_number
from flows.syriatelCashWithdrawal.valueState import get_value
WITHDRAW_NUMBER ,VALUE = [1,2]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^syriatel_cash_withdraw$')],
        states={
            WITHDRAW_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_withdraw_number)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_value)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler