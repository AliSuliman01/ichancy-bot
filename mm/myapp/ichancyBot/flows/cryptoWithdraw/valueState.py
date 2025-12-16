import Logger
from telegram import   Update
from telegram.ext import ConversationHandler,CallbackContext
from models.cryptoTransaction import CryptoTransaction
from models.user import User
from models.transaction import Transaction
from messages.withdrawMessageToAdmin import withdraw_message
from flows.cryptoWithdraw.validation.valueValidation import validate , balanceValidate
import config.crypto
from database import Database
from config.crypto import CRYPTO_WITHDRAW_GROUP
logger = Logger.getLogger()

async def get_value(update: Update, context: CallbackContext) -> int:
   db = Database.getConnection()
   try:
    if db:
        db.start_transaction()
        cursor = db.cursor(dictionary=True)
        user = update.message.from_user
        value = update.message.text
        value = value.replace('دولار','').replace('Dollar','').replace('dollar','').replace(' ','').replace('أمريكي','').replace('امريكي','').replace('USDT','')
        if validate(value):
            telegram_id = update.message.from_user.id
            user = User(cursor).getBy({'telegram_id':('=', telegram_id)})[0]
            balance = user.get('balance')
            value = float(value)
            wallet_type = context.user_data['wallet_type'] 
            currency_name , network_name = wallet_type.split("-")
            if balanceValidate(value , balance , currency_name):
                chat_id = CRYPTO_WITHDRAW_GROUP
                transfer_num = context.user_data['transfer_num']  
                user_id = user.get('id')
                # value = float(value)*float(config.crypto.SYP_for_unit[currency])
                CryptoTransaction(cursor).insert({'transfer_num' : transfer_num , 'user_id': user_id , 'status':'pending','action_type':'withdraw' , 'value' : -1*float(value)*float(config.crypto.SYP_for_unit[currency_name]) , 'currency_name' : currency_name , 'network_name' : network_name , 'SYP_for_unit' : config.crypto.SYP_for_unit[currency_name]})
                transfeer_id = cursor.lastrowid
                transfeer = CryptoTransaction(cursor).getById(transfeer_id)
                provider_type = "crypto"
                transfeer_date = transfeer['created_at']
                telegram_username = user.get('telegram_username')
                transfer_num = transfeer.get('transfer_num')
                
                Transaction(cursor).insert({'provider_id':transfeer_id ,'provider_type':provider_type,'user_id':user_id ,'value':-1*float(value)*float(config.crypto.SYP_for_unit[currency_name]) , 'action_type':'withdraw' , 'status':'pending'})
                transaction_id = cursor.lastrowid
                context.user_data["transfer_num"] = transfer_num

                message = (
                    "تم استلام طلبك وسيتم إعلامك عند معالجته\n\n"
                    f"""🆕 :طلب سحب جديد
                    🆔 رقم الطلب: #{transfeer_id}
                    📌 طريقة التحويل: {provider_type}
                    📌 العملة: {currency_name}
                    📌 الشبكة: {network_name}
                    💰 المبلغ: {value} 
                    🆔 الكود: {transfer_num}
                    👤 العضو: <a href="tg://user?id={telegram_id}">{telegram_username}</a>
                    📅 تاريخ الإنشاء: {transfeer_date}
                    """
                    )
                await update.message.reply_text(message , parse_mode='HTML')
                
                await context.bot.send_message(** withdraw_message( transaction_id = transaction_id , text = message , chat_id= chat_id))
                db.commit()
            else:
                    await update.message.reply_text("ليس لديك رصيد كافٍ")
        else:
            await update.message.reply_text("يرجى إدخال قيمة صحيحة")
        return ConversationHandler.END
   except Exception as e:
      print (e)
      db.rollback()

   finally:
      if db:
        db.close()