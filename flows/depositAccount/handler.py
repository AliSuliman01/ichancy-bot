from telegram.ext import ConversationHandler , MessageHandler ,filters ,CallbackQueryHandler ,CommandHandler
from flows.depositAccount.cancel import cancel
from flows.depositAccount.entryPoint import button_deposit_account_handler
from flows.depositAccount.ammountState import get_ammount_for_deposit
AMMOUNT = 1
def conversationHandler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_deposit_account_handler , pattern = "^deposit_account$")],
        states={
            AMMOUNT :[MessageHandler(filters.TEXT & ~filters.COMMAND , get_ammount_for_deposit)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler
