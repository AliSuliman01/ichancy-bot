from telegram.ext import filters , CallbackContext , ConversationHandler ,MessageHandler , CallbackQueryHandler ,CommandHandler,ContextTypes
from telegram import ReplyKeyboardRemove, Update 
from iChancyAPI import iChancyAPI
import config.ichancy
import flows.withdrawalAccount.entryPoint as entryPoint
import flows.withdrawalAccount.ammountState as ammountState
import flows.withdrawalAccount.cancel as cancel
AMMOUNT = 1

def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(entryPoint.button_withdrawal_from_account_handler , pattern='^withdrawal_account$')],
        states={
            AMMOUNT : [MessageHandler(filters.TEXT & ~filters.COMMAND , ammountState.get_withdraw_ammount) ]
        },
        fallbacks=[CommandHandler('cancel' , cancel.cancel)]
    )
    return conv_handler