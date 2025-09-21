from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from messages.start_message import start_message
from models.user import User
from flows.startFlow.validations.userNotExists import validation
import random , string
# import validations.start
def handler():  
    return CommandHandler('start', start)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)

    username = update.effective_user.username or update.effective_user.first_name
    if validation(user_id):
        referal_code = "".join(random.choices(string.ascii_letters + string.digits,k=5))
        x = User().getBy({'referal_code':('=',referal_code)})
        if not x:
            print("###################################################")
            User().insert({
                    'referal_code' : referal_code,
                    'telegram_id': user_id,
                    'telegram_username': username
                })
            parent_referal = update.message.text.replace('/start',"").lstrip()
            if parent_referal:
                print(parent_referal)
                parent = User().getBy({'referal_code':('=',parent_referal)})[0]
                parent_id = parent.get('id')
                User().update({'telegram_id':('=' , user_id)},{'referal_id': parent_id})
    reply_text, reply_markup = start_message()

    await update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode='Markdown')
