from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.editDepositFromAdmin.entryPoint import button_handler
from flows.editDepositFromAdmin.cancel import cancel
from flows.startFlow.handler import start
from flows.editDepositFromAdmin.getEditAmmount import get_edit_ammount
import re
EDIT = 1
def conversationHandler():

    conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern=r'^edit_deposit')],
    states={
        EDIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_edit_ammount)],
    },
    fallbacks=[CommandHandler('start',start)],
    per_chat=True,
    per_user=True,
    per_message=False,
    )    
    return conv_handler