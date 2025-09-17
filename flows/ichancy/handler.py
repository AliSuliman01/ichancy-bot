import Logger
import messages.ichancy_exist_user_message, messages.ichancy_new_user_message
import flows.ichancy.validations.userExistsInIchancy as userExist
from models.user import User
logger = Logger.getLogger()


async def handler(query , user_id) -> None:
    logger.info(f"User Click on Ichancy Option")
    await query.answer()
    if userExist.validation(user_id):
        user = User().getBy({'telegram_id':('=' , user_id)})[0]
        text , reply_markup = messages.ichancy_exist_user_message.ichancy_message(user)
    else:
        text , reply_markup = messages.ichancy_new_user_message.ichancy_message(user_id)

    await query.edit_message_text(text , reply_markup = reply_markup)


