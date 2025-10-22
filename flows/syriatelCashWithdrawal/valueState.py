import Logger
from telegram import   Update
from telegram.ext import ConversationHandler,CallbackContext
from models.syriatelTransaction import SyriatelTransaction
from models.user import User
from models.transaction import Transaction
from messages.withdrawMessageToAdmin import withdraw_message
from flows.syriatelCashWithdrawal.validation.valueValidation import balanceValidate , vlueValidate
from config.syriatel import TAX
from database import Database
logger = Logger.getLogger()

async def get_value(update: Update, context: CallbackContext) -> int:
   db = Database.getConnection()
   try:
     if db:
          db.start_transaction()
          cursor = db.cursor(dictionary=True)
          value = update.message.text
          if vlueValidate(value):
               telegram_id = update.message.from_user.id
               user = User(cursor).getBy({'telegram_id':('=', telegram_id)})[0]
               balance = user.get('balance')
               value = int(value)
               if balanceValidate(value , balance):
                    user_id = user.get('id') 
                    withdraw_number = context.user_data['withdraw_number']
                    SyriatelTransaction(cursor).insert({'transfeer_num' : withdraw_number , 'user_id': user_id , 'status':'pending','action_type':'withdraw' , 'value' : -value})
                    transfeer = SyriatelTransaction(cursor).getBy({'transfeer_num' : ('=', withdraw_number)})[0]
                    transfeer_id = transfeer.get('id')
                    transfeer_num = transfeer.get('transfeer_num')
                    provider_type = "syriatel"
                    transfeer_date = transfeer['created_at']
                    telegram_username = user.get('telegram_username')
                    Transaction(cursor).insert({'provider_id':transfeer_id ,'provider_type':provider_type,'user_id':user_id ,'value':-value , 'action_type':'withdraw' , 'status':'pending'})
                    transaction_id = Transaction(cursor).getBy({'provider_id':('=' ,transfeer_id) ,'provider_type':('=' , provider_type)})[0].get('id')
                    context.user_data["withdraw_number"] = withdraw_number

                    message =("تم استلام طلبك وسيتم إعلامك عند معالجته\n"
                    "🆕 :طلب سحب جديد\n"
                    f"   🆔 رقم الطلب: {transfeer_id}\n"
                    f"   📌 طريقة التحويل: {provider_type}\n"
                    f"   📌 الرقم: {withdraw_number}\n"
                    f"   👤 العضو: <a href='tg://user?id={telegram_id}'>{telegram_username}</a>\n"
                    f"   💰المبلغ: {value}\n"
                    f"   💰النسبة المئوية للاقتطاع: {TAX*100}%\n"
                    f"   💰المبلغ المقتطع: {value*TAX}\n"
                    f"   💰 المبلغ المستحق بعد الاقتطاع: {value - value*TAX} SYP\n"
                    f"   📅 تاريخ الإنشاء: {transfeer_date}\n"
                    )
                    
                    await update.message.reply_text(message , parse_mode="HTML")
               
                    await context.bot.send_message(** withdraw_message(telegram_id=telegram_id,transfeer_id=transfeer_id,provider_type=provider_type,telegram_username=telegram_username,value=value ,transfeer_date=transfeer_date , transaction_id = transaction_id , TAX = TAX,withdraw_number=withdraw_number , transfeer_num = transfeer_num ,text = message))  
               else:
                    await update.message.reply_text("ليس لديك رصيد كافٍ")
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