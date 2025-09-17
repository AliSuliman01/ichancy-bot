from telegram import Update 
from telegram.ext import ConversationHandler ,CallbackContext 
from models.user import User
from models.gift import Gift
from datetime import datetime
from flows.resieveGifts.validation.theCodeIsSuccess import validate
async def get_code(update:Update , context:CallbackContext):
    
    code = update.message.text
    telegram_id = update.message.from_user.id
    gift = validate(code , telegram_id)
    if gift:
        giftId = gift.get('id')
        giftAmmount = gift.get('ammount')
        oldBalance = User().getBy({'telegram_id' : ('=' , telegram_id)})[0].get('balance')
        newBalance = giftAmmount + oldBalance
        User().update({'telegram_id': ('=' , telegram_id)}, {'balance' : newBalance})
        Gift().update({'id' : ('=' , giftId)},{'redeemed_at' : datetime.now()})
        await update.message.reply_text("تمت العملية بنجاح")
    else:
        await update.message.reply_text("الكود الذي تم إدخاله غير صحيح")
    return ConversationHandler.END