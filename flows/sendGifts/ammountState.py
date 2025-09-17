from telegram import Update 
from telegram.ext import CallbackContext
import Logger
import string
from models.gift import Gift
from models.user import User
import Logger
from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
import random
import Logger
from flows.sendGifts.validation.ammountIsSuffecient import ammountIsSuffecient
from flows.sendGifts.validation.isDigit import isDigit
logger = Logger.getLogger()    

async def get_gift_ammount(update: Update, context: CallbackContext) -> int: 
    giftAmmount = update.message.text
    telegramIdGoal = context.user_data.get('telegramIdGoal')
   
    telegram_id = str(update.effective_user.id)
    user = User().getBy({'telegram_id' : ('=' , telegram_id)})[0]
    oldBalance = user.get('balance')
    if isDigit(giftAmmount):
        giftAmmount = int(giftAmmount)
        if ammountIsSuffecient(oldBalance , giftAmmount):
            newBalance = oldBalance - giftAmmount
            code = ''.join(random.choices(string.ascii_letters + string.digits,k=20))
            User().update({'telegram_id' : ('=' , telegram_id)},{'balance' : newBalance})
            Gift().insert({ 'telegram_goal_id' : telegramIdGoal ,
                            'ammount' : giftAmmount,
                            'user_id' : user.get('id'),
                            'code' : code})
            logger.info("User %s chose gift_ammount: %s", user.get('username'), giftAmmount)
            await update.message.reply_text(
                    "تمت العملية بنجاح ! \n\n"
                    "كود الهدية هو : \n\n"
                    f"`{code}` \n\n"
                    "يمكنك استخدامه للحصول على الهدية",parse_mode='Markdown'
                )
            return ConversationHandler.END
        else:
            await update.message.reply_text(
                "ليس معك رصيد كافِ \n\n"
                "يرجى تعبئة الرصيد"
            )
        return ConversationHandler.END
    else:
        await update.message.reply_text("يرجى إدخال رقم صحيح !")
        return ConversationHandler.END