import Logger
from models.transaction import Transaction
from models.user import User
from messages.depositLog import deposit_log_message
from database import Database
logger = Logger.getLogger()

async def handler(query , context):
    db = Database.getConnection()
    cursor = db.cursor(dictionary = True)
    logger.info("from deposit log handler")

    telegram_id = query.from_user.id
    print(telegram_id)
    user = User(cursor).getBy({'telegram_id' : ('=', telegram_id)})[0]
    user_id = user.get('id')
    transactions = Transaction(cursor).getBy({'user_id' : ('=' , user_id) , 'action_type' :('=' , "deposit")})
    
    if len(query.data.split(" "))==1:
        page = 0
    else: 
        page = int(query.data.split(" ")[1]) +1
    text , reply_markup = deposit_log_message(transactions , page)
    logger.info("passed get deposit log message successfully")
    if text:
             print(query.data)
             await context.bot.send_message(chat_id = telegram_id , text = text, reply_markup= reply_markup)  
    else:
         await context.bot.send_message(chat_id = telegram_id , text = "لا يوجد عمليات شحن" , reply_markup= reply_markup)