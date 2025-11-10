from telegram import  Update
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )

NAME = 2
async def get_company_name(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['company_name'] = query.data
    await query.edit_message_text("أرسل الاسم الثلاثي الذي ترغب في إرسال الأموال إليه")
    return NAME

    