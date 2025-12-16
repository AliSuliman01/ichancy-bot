import Logger
from telegram import   Update
from telegram.ext import ConversationHandler,CallbackContext
from models.shamCashTransaction import ShamCashTransaction
from models.user import User
from models.transaction import Transaction
from messages.depositMessageToAdmin import deposit_message
from flows.shamCashDepodit.validation.valueValidation import validate
from database import Database
from config.shamCash import SHAMCASH_DEPOSIT_GROUP
logger = Logger.getLogger()

async def get_value(update: Update, context: CallbackContext) -> int:
   db = Database.getConnection()
   try:
    if db:
        db.start_transaction()
        cursor = db.cursor(dictionary=True)
        user = update.message.from_user
        value = update.message.text

        if validate(value):
            transfer_num = context.user_data['transfer_num']
            telegram_id = update.message.from_user.id
            user = User(cursor).getBy({'telegram_id':('=', telegram_id)})[0]
            user_id = user.get('id')
            ShamCashTransaction(cursor).insert({'transfer_num' : transfer_num , 'user_id': user_id , 'status':'pending','action_type':'deposit' , 'value' : value})
            chat_id = SHAMCASH_DEPOSIT_GROUP
            transfeer = ShamCashTransaction(cursor).getBy({'transfer_num' : ('=', transfer_num)})[0]
            transfeer_id = transfeer.get('id')
            provider_type = "sham cash"
            transfeer_date = transfeer['created_at']
            telegram_username = user.get('telegram_username')
            
            
            Transaction(cursor).insert({'provider_id':transfeer_id ,'provider_type':provider_type,'user_id':user_id ,'value':value , 'action_type':'deposit' , 'status':'pending'})
            transaction_id = Transaction(cursor).getBy({'provider_id':('=' ,transfeer_id) ,'provider_type':('=' , provider_type)})[0].get('id')
            context.user_data["transfer_num"] = transfer_num

            message = (
                "تم استلام طلبك وسيتم إعلامك عند معالجته\n\n"
                f"""🆕 :طلب شحن جديد
                🆔 رقم الطلب: #{transfeer_id}
                📌 طريقة التحويل: {provider_type}
                🆔 الكود: {transfer_num}
                💰 المبلغ: {value} SYP
                👤 العضو: <a href='tg://user?id={telegram_id}'>{telegram_username}</a>
                📅 تاريخ الإنشاء: {transfeer_date}
                """
                )
            await update.message.reply_text(message , parse_mode='HTML')
            
            await context.bot.send_message(** deposit_message(value=value , transaction_id = transaction_id , text = message , chat_id= chat_id))

        else:
            await update.message.reply_text("يرجى إدخال قيمة صحيحة")
        db.commit()
        return ConversationHandler.END
   except Exception as e:
      print (e)
      db.rollback()

   finally:
      if db:
        db.close()