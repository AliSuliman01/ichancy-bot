from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.editDepositFromAdmin.entryPoint import button_handler
from flows.editDepositFromAdmin.cancel import cancel
from flows.editDepositFromAdmin.getEditAmmount import get_edit_ammount
import re
EDIT = 1
def conversationHandler():

    conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern=r'^edit')],
    states={
        EDIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_edit_ammount)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )    
    return conv_handler