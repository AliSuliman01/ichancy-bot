from telegram.ext import ConversationHandler , ContextTypes 
from telegram import Update 
import config.telegram
from models.messageToAdmin import MessageToAdmin
from models.user import User
async def get_message(update : Update , context:ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    user = User().getBy({'telegram_id' : ('=' , telegram_id)})[0]
    user_id = user.get('id')
    
    media = update.message.photo
    photo = None

    if media:
        photo = update.message.photo[0].file_id
        message = update.message.caption or " "
        MessageToAdmin().insert({'user_id' : user_id , 'message': message , 'photo' : photo})
    else:
        message = update.message.text
        MessageToAdmin().insert({'user_id' : user_id , 'message': message})

    

    await update.message.reply_text("تم إرسال الرسالة للأدمن") 
    if photo:
        await context.bot.send_photo(chat_id=config.telegram.ADMIN_ID, caption=message ,photo=photo)
    else:
        await context.bot.send_message(chat_id=config.telegram.ADMIN_ID, text=message)  

    return ConversationHandler.END
