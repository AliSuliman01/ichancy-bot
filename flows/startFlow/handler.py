from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from messages.start_message import start_message
from models.user import User
from flows.startFlow.validations.userNotExists import validation
import random , string
# import validations.start
from database import Database
def handler():  
    return CommandHandler('start', start)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  db = Database.getConnection()
  try:
    if db:
        db.start_transaction()
        cursor = db.cursor(dictionary=True)
        user_id = str(update.effective_user.id)

        username = update.effective_user.username or update.effective_user.first_name
        if validation(user_id , cursor):
            referal_code = "".join(random.choices(string.ascii_letters + string.digits,k=5))
            x = User(cursor).getBy({'referal_code':('=',referal_code)})
            if not x:
                User(cursor).insert({
                        'referal_code' : referal_code,
                        'telegram_id': user_id,
                        'telegram_username': username
                    })
                parent_referal = update.message.text.replace('/start',"").lstrip()
                if parent_referal:
                    print(parent_referal)
                    parent = User(cursor).getBy({'referal_code':('=',parent_referal)})[0]
                    parent_id = parent.get('id')
                    User(cursor).update({'telegram_id':('=' , user_id)},{'referal_id': parent_id})
        reply_text, reply_markup = start_message()
        db.commit()
        await update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode='Markdown')
  except Exception as e:
     print (e)
     db.rollback()
  finally:
     if db:
         db.close()