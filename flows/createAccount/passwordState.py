import string
from iChancyAPI import iChancyAPI
import asyncio
import Logger 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ContextTypes,ConversationHandler,CallbackContext,MessageHandler,filters,CommandHandler,CallbackQueryHandler)
from models.user import User
import random

logger = Logger.getLogger()


async def get_password(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    print(user)
    password = update.message.text
    logger.info("User %s set password: %s", user.first_name, password)
    try:
        user_id = str(user.id)
        email=context.user_data.get('email')
        username=context.user_data.get('username')
        api = iChancyAPI()

        logger.info(api.COOKIES)
        result = api.register_account(email=email, username=username, password=password)
        count = 1
        while not result['success'] and count <15:
            count+=1
            username=context.user_data.get('username')+ "_"+ ''.join(random.choices(string.ascii_letters + string.digits,k=3))
            email = username + "@gilbert.com"
            result = api.register_account(email=email, username=username, password=password)


        if result['success']:
            playerId = api.getPlayerId(username)    
            User().update({'telegram_id':("=" , user_id)},{'password' : password ,'email':email,'player_id':playerId ,'name':username})
            keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            success_text = (
                f"✅ **تم إنشاءالحساب بجاح !** \n\n"
                f"🆔 **الدخول**: `{result['username']}`\n"
                f"🔒 **كلمة المرور**: `{result['password']}`\n"
                f"📧 **الإيميل**: `{result['email']}`\n"
            )
            
            await update.message.reply_text(success_text ,parse_mode='Markdown')
        else:
            keyboard = [[InlineKeyboardButton("🔄 Try Again", callback_data='create_account'),
                        InlineKeyboardButton("🏠 Menu", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            error_msg = result['error']
            error_msg = error_msg.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('(', '\\(').replace(')', '\\)').replace('~', '\\~').replace('`', '\\`').replace('>', '\\>').replace('#', '\\#').replace('+', '\\+').replace('-', '\\-').replace('=', '\\=').replace('|', '\\|').replace('{', '\\{').replace('}', '\\}').replace('.', '\\.').replace('!', '\\!')
            keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"❌ **Account Creation Failed**\n\n"
                f"Error: {error_msg}\n\n"
                "You can try again or return to the main menu.",
                reply_markup=reply_markup,
                parse_mode='Markdown'
                
            )
    except Exception as e:
        logger.error(f"Error in handle_create_account: {e}")
        keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"❌ **An error occurred**: {str(e)}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    return ConversationHandler.END
