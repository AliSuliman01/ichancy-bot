from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
import config.crypto
from flows.cryptoWithdraw.entryPoint import button_handler
from flows.cryptoWithdraw.cancel import cancel
from flows.startFlow.handler import start
from flows.cryptoWithdraw.walletTypeState import get_wallet_type
from flows.cryptoWithdraw.valueState import get_value
from flows.cryptoWithdraw.transfeerNumState import get_transfer_num
from flows.backToMenu.handler import handler
WALLET_TYPE , transfer_num , VALUE  = [1 , 2 , 3]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^crypto_withdraw$')],
        states={
            WALLET_TYPE: [CallbackQueryHandler(get_wallet_type , pattern=config.crypto.WALLET_TYPE)],
            transfer_num: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transfer_num)],
            VALUE:[MessageHandler(filters.TEXT & ~filters.COMMAND , get_value)]
        },
        #cus we have a callback query that have backToMenu and Doesnt end the ConversationHandler
        fallbacks=[CommandHandler('start',start) , CallbackQueryHandler(handler, pattern='^back_to_menu$')],
        per_chat=True,
        per_user=True,
        per_message=False,
    )
    return conv_handler