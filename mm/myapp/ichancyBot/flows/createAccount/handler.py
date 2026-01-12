import Logger 
from telegram import Update
from telegram.ext import (ContextTypes,ConversationHandler,MessageHandler,filters,CommandHandler,CallbackQueryHandler)
from flows.createAccount.cancel import cancel
from flows.startFlow.handler import start
from flows.createAccount.entryPoint import button_handler
from flows.createAccount.passwordState import get_password
from flows.createAccount.userNameState import get_username
from iChancyAPI import iChancyAPI
import asyncio
import config.telegram
import string
import random
from models.user import User
from database import Database
logger = Logger.getLogger()

USERNAME, PASSWORD = [1,2]

def conversationHandler():
    conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern='^create_account$')],
    states={
        USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
        PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
    },
    fallbacks=[CommandHandler('start',start)],
    per_chat=True,
    per_user=True,
    per_message=False,
    )    
    return conv_handler



async def finishingHandler(update:Update , context):
   db = Database.getConnection()
   try:
    if db:
        # logger.info("in handler for create cookie")
        db.start_transaction()
        cursor = db.cursor(dictionary = True)
        user = update.message.from_user
        password = update.message.text
        user_id = str(user.id)
        username=context.user_data.get('username')
        # logger.info("User %s set password: %s", user.first_name, password)
        counter = 0
        while True:
            # logger.info("in ////while////handler for create cookie")
            counter+=1
            
            # Check cookie status first - if False, wait a bit then check again
            if not config.telegram.COOKIE_STATUS:
                if counter == 1:
                    # First check - try to validate cookie
                    api = iChancyAPI()
                    cookie_check = api.checkCookieIsWork()
                    if cookie_check.get('success'):
                        config.telegram.COOKIE_STATUS = True
                    else:
                        # Cookie is invalid, inform user immediately
                        await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                        await update.message.reply_text("هذه الخدمة في حالة الصيانة \n\n الوقت المتوقع لتعود متاحة 5 دقائق")
                        db.rollback()
                        return
                
                # If still False after first check, wait and retry
                if counter > 8:  # Wait max 40 seconds (8 * 5)
                    await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                    await update.message.reply_text("هذه الخدمة في حالة الصيانة \n\n الوقت المتوقع لتعود متاحة 5 دقائق")
                    db.rollback()
                    return
                await asyncio.sleep(5)
                continue
            
            # Cookie status is True, proceed with registration
            api = iChancyAPI()
            username=context.user_data.get('username')+ "_"+ ''.join(random.choices(string.ascii_letters + string.digits,k=5))
            email = username + "@gilbert.com"
            
            try:
                result = await api.register_account(email=email, username=username, password=password)
            except Exception as e:
                logger.error(f"Exception during registration: {e}", exc_info=True)
                result = {'success': False, 'error': str(e)}
            
            if result.get('success'):
                await asyncio.sleep(0.2)             
                playerIdInfo = await api.getPlayerId(username)
                if playerIdInfo['success'] :  
                    playerId = playerIdInfo['data']  
                    User(cursor).update({'telegram_id':("=" , user_id)},{'password' : password ,'email':email,'player_id':playerId ,'name':username})
                    success_text = (
                    f"✅ **تم إنشاءالحساب بجاح !** \n\n"
                    f"🆔 **الدخول**: `{result['username']}`\n"
                    f"🔒 **كلمة المرور**: `{result['password']}`\n"
                    f"📧 **الإيميل**: `{result['email']}`\n"
                    )
                    await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                    await update.message.reply_text(success_text ,parse_mode='Markdown')
                    db.commit()
                    break
            else:
                # Registration failed - check if it's a cookie issue
                error_msg = result.get('error', 'Unknown error')
                if 'challenge' in error_msg.lower() or 'cloudflare' in error_msg.lower():
                    config.telegram.COOKIE_STATUS = False
                    await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                    await update.message.reply_text("هذه الخدمة في حالة الصيانة \n\n الوقت المتوقع لتعود متاحة 5 دقائق")
                    db.rollback()
                    return
                # Other errors - log and retry
                logger.warning(f"Registration failed: {error_msg}, retrying...")
            
            if counter > 40:
                await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                await update.message.reply_text("هذه الخدمة في حالة الصيانة \n\n الوقت المتوقع لتعود متاحة 5 دقائق")
                db.rollback()
                return
            await asyncio.sleep(5)
   except Exception as e:
       logger.error(f"Error in createAccount handler: {e}")
       db.rollback()

   finally:
       if db:
        db.close()