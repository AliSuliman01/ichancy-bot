from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.editWithdrawFromAdmin.entryPoint import button_handler
from flows.editWithdrawFromAdmin.cancel import cancel
from flows.editWithdrawFromAdmin.getEditAmmount import get_edit_ammount
EDIT = 1
def conversationHandler():

    conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern=r'^edit_withdraw')],
    states={
        EDIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_edit_ammount)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )    
    return conv_handler