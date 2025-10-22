from telegram import Update 
from telegram.ext import ConversationHandler ,CallbackContext 
from models.user import User
from models.gift import Gift
from datetime import datetime
from flows.resieveGifts.validation.theCodeIsSuccess import validate
from database import Database
async def get_code(update:Update , context:CallbackContext):
   db = Database.getConnection()
   try:
    if db:
        db.start_transaction()
        cursor = db.cursor(dictionary = True)
        code = update.message.text
        telegram_id = update.message.from_user.id
        gift = validate(code , telegram_id)
        if gift:
            giftId = gift.get('id')
            giftAmmount = gift.get('ammount')
            oldBalance = User(cursor).getBy({'telegram_id' : ('=' , telegram_id)})[0].get('balance')
            newBalance = giftAmmount + oldBalance
            User(cursor).update({'telegram_id': ('=' , telegram_id)}, {'balance' : newBalance})
            Gift(cursor).update({'id' : ('=' , giftId)},{'redeemed_at' : datetime.now()})
            await update.message.reply_text("تمت العملية بنجاح")
        else:
            await update.message.reply_text("الكود الذي تم إدخاله غير صحيح")
        db.commit()
        return ConversationHandler.END
   except Exception as e:
      print (e)
      db.rollback()
    
   finally:
      if db:
        db.close()