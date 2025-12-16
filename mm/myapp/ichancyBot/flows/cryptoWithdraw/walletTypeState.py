from telegram import  Update
from telegram.ext import CallbackContext ,ConversationHandler
import Logger
logger = Logger.getLogger()
transfer_num = 2

async def get_wallet_type(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    # print(query)
    # print("#"*40)
    await query.answer()
    wallet_type = query.data
    context.user_data["wallet_type"] = wallet_type
    await query.edit_message_text("أرسل الحساب الذي ترغب في استقبال ارباحك عليه" )
    return transfer_num

