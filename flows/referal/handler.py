
import messages.referal
from models.user import User
import Logger
from datetime import datetime , timedelta
import config.referal 
from database import Database
logger = Logger.getLogger()
async def handler(query):
    db = Database.getConnection()
    cursor = db.cursor(dictionary = True)
    logger.info("in referal handler")
    telegram_id = query.from_user.id
    print(telegram_id)
    user_id = User(cursor).getBy({'telegram_id':('=' , telegram_id)})[0].get('id')
    num_of_referal_child = len(User(cursor).getBy({'referal_id':('=',user_id)}))  
    logger.info(f"get num of referal child in referal/handler {num_of_referal_child}")
    referal_code = User(cursor).getBy({'telegram_id':('=', telegram_id)})[0].get('referal_code')
    logger.info(f"get num of referal code in referal/handler {referal_code}")
    logger.info(f"get referal time : {config.referal.REFERAL_DATE} in referal/info")
    print(config.referal.REFERAL_DATE)
    print(datetime.now())
    x = config.referal.REFERAL_DATE - datetime.now()
    x = str(x.days) + "أيام و " + str(x.seconds//3600) + "ساعة و " + str(x.seconds%3600 //60) + "  دقيقة " 

    text , reply_markup  = messages.referal.referal_message(num_of_referal_child , referal_code , x)
    await query.message.reply_text(text , reply_markup = reply_markup)
    db.close()


