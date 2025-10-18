from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.bemoWithdrawal.entryPoint import button_handler
from flows.bemoWithdrawal.cancel import cancel
from flows.bemoWithdrawal.withdrawNumberState import get_withdraw_number
from flows.bemoWithdrawal.valueState import get_value
WITHDRAW_NUMBER ,VALUE = [1,2]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^bemo_withdrawal$')],
        states={
            WITHDRAW_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_withdraw_number)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_value)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler