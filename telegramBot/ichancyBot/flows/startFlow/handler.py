from telegram import Update
from telegram.ext import CommandHandler, ContextTypes , ConversationHandler
from messages.start_message import start_message
from models.user import User
from flows.startFlow.validations.userNotExists import validation
import random , string
from config.telegram import TELEGRAM_CHANNELS , TELEGRAM_GROUPS 
# import validations.start
from database import Database
from Logger import getLogger
def handler():  
    return CommandHandler('start', start)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  logger = getLogger()
  print("#"*40)
  print(update.effective_user)
  if update.effective_user.id:
     context.application.drop_user_data(update.effective_user.id)

  is_in_channel = True 
  is_in_group = True
  for CHANNEL_USERNAME in TELEGRAM_CHANNELS :
    try:
            channel_member = await context.bot.get_chat_member(CHANNEL_USERNAME, update.effective_user.id)
            is_in_channel = channel_member.status in ["member", "administrator", "creator"]
            if not is_in_channel:
                await context.bot.send_message(
                chat_id=update.effective_user.id,
                text=f"عذرا عزيزي\n\nيجب عليك الاشتراك بالقناة التالية قبل استخدام البوت\n\n {CHANNEL_USERNAME}")
                break
    except Exception as e:
            logger.error(f"Error checking channel: {e}")
            break   

  if is_in_channel:
    for GROUP_USERNAME in TELEGRAM_GROUPS:
      
        try:
                group_member = await context.bot.get_chat_member(GROUP_USERNAME, update.effective_user.id)
                print(group_member)
                is_in_group = group_member.status in ["member", "administrator", "creator"]
                if not is_in_group :
                    await context.bot.send_message(
                    chat_id=update.effective_user.id,
                    text=f"عذرا عزيزي\n\nيجب عليك الاشتراك بالمجموعة التالية قبل استخدام البوت\n\n {GROUP_USERNAME}")
                    break
        except Exception as e:
                logger.error(f"Error checking group: {e}")
                break
  else:
        is_in_group = False

  if is_in_group:
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
            return ConversationHandler.END
    except Exception as e:
        print (e)
        db.rollback()
    finally:
        if db:
            db.close()