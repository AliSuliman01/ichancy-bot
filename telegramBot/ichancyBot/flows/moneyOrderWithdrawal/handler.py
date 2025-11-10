from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.moneyOrderWithdrawal.entryPoint import button_handler
from flows.moneyOrderWithdrawal.cancel import cancel
from flows.startFlow.handler import start
from flows.moneyOrderWithdrawal.companyNameState import get_company_name
from flows.moneyOrderWithdrawal.valueState import get_value
from flows.moneyOrderWithdrawal.nameState import get_name
from flows.moneyOrderWithdrawal.cityNameState import get_city_name
from flows.moneyOrderWithdrawal.phoneNumberState import get_phone_number
from flows.backToMenu.handler import handler
# WITHDRAW_CITY_NAME ,VALUE = [1,2]
COMPANY_NAME,NAME,CITY_NAME,PHONE_NUMBER,VALUE =  [1,2,3,4,5]
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^order_money_withdrawal$')],
        states={
            # WITHDRAW_CITY_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_)],
            COMPANY_NAME: [CallbackQueryHandler(get_company_name , pattern = r'haram|qadmous')],
            NAME:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CITY_NAME:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_city_name)],
            PHONE_NUMBER:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_number)],
            VALUE:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_value)],
        },
        fallbacks=[CommandHandler('start',start) , CallbackQueryHandler(handler, pattern='^back_to_menu$')],
    )
    return conv_handler