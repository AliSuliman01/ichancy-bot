from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.shamCashWithdrawal.entryPoint import button_handler
from flows.shamCashWithdrawal.cancel import cancel
from flows.startFlow.handler import start
from flows.shamCashWithdrawal.withdrawNumberState import get_withdraw_number
from flows.shamCashWithdrawal.valueState import get_value
WITHDRAW_NUMBER ,VALUE = [1,2]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^sham_cash_withdrawal$')],
        states={
            WITHDRAW_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_withdraw_number)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_value)],
        },
        fallbacks=[CommandHandler('start',start)],
        per_chat=True,
        per_user=True,
        per_message=False,
    )
    return conv_handler