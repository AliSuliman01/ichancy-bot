import Logger
from telegram import  InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler,CallbackContext
from models.syriatelTransaction import SyriatelTransaction
from models.user import User
from models.transaction import Transaction
from messages.depositMessageToAdmin import deposit_message
logger = Logger.getLogger()

async def get_value(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    value = update.message.text
    if str.isdigit(value):
        transfeer_num = context.user_data['transfeer_num']
        telegram_id = update.message.from_user.id
        user = User().getBy({'telegram_id':('=', telegram_id)})[0]
        user_id = user.get('id')
        SyriatelTransaction().insert({'transfeer_num' : transfeer_num , 'user_id': user_id , 'status':'pending','action_type':'deposit' , 'value' : value})
        transfeer = SyriatelTransaction().getBy({'transfeer_num' : ('=', transfeer_num)})[0]
        transfeer_id = transfeer.get('id')
        transfeer_function = "Syriatel Cash 🟢"
        transfeer_date = transfeer['created_at']
        telegram_username = user.get('telegram_username')
        message = (
            "تم استلام طلبك وسيتم إعلامك عند معالجته\n\n"
            f"""🆕 :طلب شحن جديد
            🆔 رقم الطلب: #{transfeer_id}
            📌 طريقة التحويل: {transfeer_function}
            💰 المبلغ: {value} SYP
            📅 تاريخ الإنشاء: {transfeer['created_at']}
            """
            )
        await update.message.reply_text(message)
        await context.bot.send_message(**deposit_message(telegram_id=telegram_id,transfeer_id=transfeer_id,transfeer_function=transfeer_function,telegram_username=telegram_username,value=value ,transfeer_date=transfeer_date))  
    else:
         await update.message.reply_text("يرجى إدخال قيمة صحيحة")
    return ConversationHandler.END
