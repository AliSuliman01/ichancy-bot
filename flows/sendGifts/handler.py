from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)
from flows.sendGifts.telegramIdGoalState import get_telegram_id_goal
from flows.sendGifts.ammountState import get_gift_ammount
from flows.sendGifts.entryPoint import button_send_gifts_handler
from flows.sendGifts.cancel import cancel
telegramIdGoal , ammount = [1,2]
def conversationHandler():
    conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_send_gifts_handler, pattern='^send_gift$')],
    states={
        telegramIdGoal: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_telegram_id_goal)],
        ammount: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_gift_ammount)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )    
    return conv_handler