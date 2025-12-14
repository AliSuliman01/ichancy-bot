from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
import config.crypto
from flows.cryptoDeposit.entryPoint import button_handler
from flows.cryptoDeposit.cancel import cancel
from flows.startFlow.handler import start
from flows.backToMenu.handler import handler
from flows.cryptoDeposit.walletTypeState import get_wallet_type
from flows.cryptoDeposit.valueState import get_value
from flows.cryptoDeposit.transfeerNumState import get_transfeer_num
WALLET_TYPE , TRANSFEER_NUM , VALUE  = [1 , 2 , 3]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^crypto_deposit$')],
        states={
            WALLET_TYPE: [CallbackQueryHandler(get_wallet_type , pattern=config.crypto.WALLET_TYPE)],
            TRANSFEER_NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transfeer_num)],
            VALUE:[MessageHandler(filters.TEXT & ~filters.COMMAND , get_value)]
        },
         fallbacks=[CommandHandler('start',start) , CallbackQueryHandler(handler, pattern='^back_to_menu$')],
         per_chat=True,
         per_user=True,
         per_message=False,
    )
    return conv_handler