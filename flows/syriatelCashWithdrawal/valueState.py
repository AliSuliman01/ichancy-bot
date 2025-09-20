import Logger
from telegram import   Update
from telegram.ext import ConversationHandler,CallbackContext
from models.syriatelTransaction import SyriatelTransaction
from models.user import User
from models.transaction import Transaction
from messages.withdrawMessageToAdmin import withdraw_message
from flows.syriatelCashWithdrawal.validation.valueValidation import balanceValidate , vlueValidate
from config.syriatel import TAX
logger = Logger.getLogger()

async def get_value(update: Update, context: CallbackContext) -> int:
     value = update.message.text

     if vlueValidate(value):
          telegram_id = update.message.from_user.id
          user = User().getBy({'telegram_id':('=', telegram_id)})[0]
          balance = user.get('balance')
          value = int(value)
          if balanceValidate(value , balance):
               user_id = user.get('id') 
               withdraw_number = context.user_data['withdraw_number']
               SyriatelTransaction().insert({'transfeer_num' : withdraw_number , 'user_id': user_id , 'status':'pending','action_type':'withdraw' , 'value' : -value})
               transfeer = SyriatelTransaction().getBy({'transfeer_num' : ('=', withdraw_number)})[0]
               transfeer_id = transfeer.get('id')
               provider_type = "syriatel"
               transfeer_date = transfeer['created_at']
               telegram_username = user.get('telegram_username')
               Transaction().insert({'provider_id':transfeer_id ,'provider_type':provider_type,'user_id':user_id ,'value':-value , 'action_type':'withdraw' , 'status':'pending'})
               transaction_id = Transaction().getBy({'provider_id':('=' ,transfeer_id) ,'provider_type':('=' , provider_type)})[0].get('id')
               context.user_data["withdraw_number"] = withdraw_number

               message = (
                    "تم استلام طلبك وسيتم إعلامك عند معالجته\n\n"
                    f"""
                    🆕 :طلب سحب جديد
                    🆔 رقم الطلب: #{transfeer_id}
                    📌 طريقة التحويل: {provider_type}
                    📌 الرقم: {withdraw_number}
                    👤 العضو: <a href="tg://user?id={telegram_id}">{telegram_username}</a>
                    💰المبلغ: {value}
                    💰النسبة المئوية للاقتطاع: {TAX*100}%
                    💰المبلغ المقتطع: {value*TAX}
                    💰 المبلغ المستحق بعد الاقتطاع: {value - value*TAX} SYP
                    📅 تاريخ الإنشاء: {transfeer_date}
                    """
                         )
               await update.message.reply_text(message , parse_mode="HTML")
          
               await context.bot.send_message(** withdraw_message(telegram_id=telegram_id,transfeer_id=transfeer_id,provider_type=provider_type,telegram_username=telegram_username,value=value ,transfeer_date=transfeer_date , transaction_id = transaction_id , TAX = TAX,withdraw_number=withdraw_number))  
          else:
               await update.message.reply_text("ليس لديك رصيد كافٍ")
     else:
          await update.message.reply_text("يرجى إدخال قيمة صحيحة")
     return ConversationHandler.END
