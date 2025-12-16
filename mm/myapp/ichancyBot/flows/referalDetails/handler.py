
import messages.referal_details
from models.user import User
import Logger
from datetime import datetime , timedelta
import config.referal
from models.transaction import Transaction
from database import Database
logger = Logger.getLogger()
async def handler(query):
     db = Database.getConnection()
     try:
          if db:
               cursor = db.cursor(dictionary = True)
               num_of_activate_referal_child = 0
               value_from_referals = 0
               # logger.info("in referal details handler")
               telegram_id = query.from_user.id
               user_id = User(cursor).getBy({'telegram_id':('=' , telegram_id)})[0].get('id')
               referal_child = User(cursor).getBy({'referal_id':('=',user_id)})
               num_of_referal_child = len(referal_child)  
               # logger.info(f"get num of referal child in referal/handler {num_of_referal_child}")
               for child in referal_child:
                    child_id = child.get('id')
                    child_transactions = Transaction(cursor).getBy({'user_id':('=' , child_id) ,'created_at' : (">" , config.referal.REFERAL_DATE - timedelta(**config.referal.ROLL_TIME)) 
                                                                 , 'status':('=' , 'approved')})  

                    if child_transactions:
                         num_of_activate_referal_child+=1
                         for child_transaction in child_transactions:
                              value_from_referals+= abs(child_transaction.get('value'))*config.referal.REFERAL_PERCENT
               # logger.info(f"number of activate child referal = {num_of_activate_referal_child} for user {user_id}")
               if num_of_activate_referal_child < config.referal.MIN_NUM_OF_REFERALS:
                    value_from_referals = 0
               # logger.info(f"get all referal value from transactions {value_from_referals}")

               referal_code = User(cursor).getBy({'telegram_id':('=', telegram_id)})[0].get('referal_code')
               # logger.info(f"get num of referal code in referal/handler {referal_code}")
               # print(config.referal.REFERAL_DATE)
               # logger.info(f"get referal time : {config.referal.REFERAL_DATE} in referal/info")
               referal_time_needed = config.referal.REFERAL_DATE - datetime.now()
               referal_time_needed = str(referal_time_needed.days) + "يوم " + str(referal_time_needed.seconds//3600) + "ساعة " + str(referal_time_needed.seconds%3600 //60) + " دقيقة   " + str(referal_time_needed.seconds%60)

               text , reply_markup  = messages.referal_details.referal_message(num_of_activate_referal_child , referal_code , referal_time_needed,value_from_referals)
               await query.message.reply_text(text , reply_markup = reply_markup)
     except:
          ""
     finally:
          if db:
               db.close()


