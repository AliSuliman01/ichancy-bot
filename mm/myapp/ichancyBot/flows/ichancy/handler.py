import Logger
import messages.ichancy_exist_user_message, messages.ichancy_new_user_message
import flows.ichancy.validations.userExistsInIchancy as userExist
from models.user import User
logger = Logger.getLogger()
from database import Database
async def handler(query , user_id) -> None:
    db = Database.getConnection()
    try:
        if db:

            cursor = db.cursor(dictionary = True)
            # logger.info(f"User Click on Ichancy Option")
            await query.answer()
            # if not config.telegram.COOKIE_STATUS:
            #     await query.edit_message_text("عملية صيانة دورية للبوت وسيتم إعادة تشغيله خلال بضع دقائق")
            #     return
            if userExist.validation(user_id):
                user = User(cursor).getBy({'telegram_id':('=' , user_id)})[0]
                text , reply_markup = messages.ichancy_exist_user_message.ichancy_message(user)
            else:
                text , reply_markup = messages.ichancy_new_user_message.ichancy_message(user_id)

            await query.edit_message_text(text , reply_markup = reply_markup)
    except:
        ""

    finally:
        db.close()
