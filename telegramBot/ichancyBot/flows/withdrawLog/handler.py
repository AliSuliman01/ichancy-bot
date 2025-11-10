import Logger
from models.transaction import Transaction
from models.user import User
from messages.withdrawLog import withdraw_log_message
from database import Database
logger = Logger.getLogger()


async def handler(query , context):
    db = Database.getConnection()
    try:
        if db:

            cursor = db.cursor(dictionary = True)
            logger.info("from withdraw log handler")

            telegram_id = query.from_user.id
            print(telegram_id)
            user = User(cursor).getBy({'telegram_id' : ('=', telegram_id)})[0]
            user_id = user.get('id')
            transactions = Transaction(cursor).getBy({'user_id' : ('=' , user_id) , 'action_type' :('=' , "withdraw")})

            if len(query.data.split(" "))==1:
                page = 0
                print(page)
            else: 
                page = int(query.data.split(" ")[1]) +1
                print(page)
                print("from else")
            text , reply_markup = withdraw_log_message(transactions , page)
            logger.info("passed get withdraw log message successfully")
            
            await context.bot.send_message(chat_id = telegram_id , text = text , reply_markup= reply_markup)  

    except:
        ""
    finally:
        if db:
            db.close()

