import asyncio
import logging
from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    CallbackContext,
    MessageHandler,
    filters
)
import requests
from bs4 import BeautifulSoup
import random
import string
import json
import os
import time
import store

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7985162765:AAEg_aQ-cLRMxLVzAeTwu7_EIgn81THL_BM')
# SESSION_FILE = 'ichancy_sessions.json'
COOKIE_STRING = 'PHPSESSID_3a07edcde6f57a008f3251235df79776a424dd7623e40d4250e37e4f1f15fadf=bd652b7e6716d615eba9080694540023; languageCode=en_GB; language=English%20%28UK%29; __cf_bm=uT4L541q35h7tOaGEsSe8boADjo7jjsMJQuRUUd1rBE-1757326114-1.0.1.1-966UdZ_peu6MLm1syB58WHBqE2IFkzghidGjNJghH7idByy3kAYxzJCqC5s4C1yKLAPm9uZPDrR0pur9cxjJUv.xl16mwODCHv444odp8PI; cf_clearance=ovItEOzpTgCqkZXlvkwFxBZAuXAfiltqEFrf9IG8S_o-1757326127-1.2.1.1-BUAtJtYX4E4smvvQO1MzELJfYaNvmEN7yZfBB8XFvLw.Ntj5ugHFGM1zbuwIxrmcZOr6_lmUrjbg6VDEM1Y9toHisjLERav7tMJVkUQYEm1OdloE5ov4VXiWWzsNck.wPsx2QG2YBE2kg.Khoke3q77y2qsOO.zIlIqrJ07O6RB1uxnEA9yCR_N5teAGaWIHbINiJlcZtj.c48lYBd83Qyt9OKv3REUUt3GchSFhMik'
# Validate bot token


if not TOKEN or TOKEN.startswith('YOUR_BOT_TOKEN'):
    logger.error("Please set TELEGRAM_BOT_TOKEN environment variable")
    exit(1)

class iChancyAPI:
    BASE_URL = 'https://www.ichancy.com'
    
    # Static headers - update these as needed
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Cookie': COOKIE_STRING,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://agents.ichancy.com',
        'Referer': 'https://agents.ichancy.com/'
    }
    
    @staticmethod
    def parse_cookie_string(cookie_string):
        """
        Parse a cookie string and return a dictionary of cookies
        Example: '__cf_bm=value1; cf_clearance=value2'
        """
        cookies = {}
        if not cookie_string:
            return cookies
            
        # Split by semicolon and process each cookie
        cookie_pairs = cookie_string.split(';')
        for pair in cookie_pairs:
            pair = pair.strip()
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookies[name.strip()] = value.strip()
        
        return cookies
    
    @classmethod
    def set_cookies_from_string(cls, cookie_string):
        """
        Set cookies from a cookie string
        """
        cls.COOKIES = cls.parse_cookie_string(cookie_string)
        logger.info(f"Updated cookies: {list(cls.COOKIES.keys())}")
    
    def __init__(self):
        
        self.session = requests.Session()
        
        self.session.headers.update(self.HEADERS)
        
        logger.info("Initialized iChancy API with headers and cookies")
        
    def register_account(self, username=None, password=None, email=None, parent_id="2495754"):
        """
        Register a new account using the iChancy API
        """
        logger.info("Starting account registration process")
        
        try:

            username = username
            password = password
            email = email 
            
            logger.info(f"Generated credentials - Username: {username}, Email: {email}")
            
            # API endpoint
            register_url = "https://agents.ichancy.com/global/api/Player/registerPlayer"
            
            # Prepare JSON payload
            payload = {
                "player": {
                    "login": username,
                    "email": email,
                    "password": password,
                    "parentId": parent_id
                }
            }
            
            
            # Log the request details for debugging
            logger.info(f"Making request to: {register_url}")
            # logger.info(f"Headers: {headers}")
            logger.info(f"Payload: {payload}")
        
            # Submit registration
            logger.info("Submitting registration to API")
            try:
                response = self.session.post(
                    register_url, 
                    json=payload, 
                    # headers=headers,
                    timeout=30
                )
                
                # Log response details for debugging
                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Response headers: {dict(response.headers)}")
                logger.info(f"Response text: {response.text[:500]}...")  # First 500 chars
                #  response.text = {"status":true,"html":"","result":false,"notification":[{"code":1,"content":"Duplicate login","title":"","autoHideAfter":5000,"list":[],"status":"error"}]}
                json = response.json()
                if not json.get("result"):
                    return {'success': False, 'error':json.get("notification")[0].get("content") }
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP Error: {e}")
                logger.error(f"Response status: {e.response.status_code}")
                
                # Check if it's a Cloudflare challenge
                if 'cf-mitigated' in e.response.headers and e.response.headers['cf-mitigated'] == 'challenge':
                    return {'success': False, 'error': 'Cloudflare challenge detected - cookies may be expired or invalid. Please get fresh cookies from your browser and update the COOKIE_STRING variable.'}
                
                # Try to decode response text safely
                try:
                    response_text = e.response.text[:200]
                except:
                    response_text = "Unable to decode response"
                
                return {'success': False, 'error': f'HTTP Error {e.response.status_code}: {response_text}'}
            except Exception as e:
                logger.error(f"Registration submission failed: {e}")
                return {'success': False, 'error': f'Registration submission failed: {str(e)}'}
            
            # Parse JSON response
            try:
                response_data = response.json()
                logger.info(f"API Response: {response_data}")
            except Exception as e:
                logger.error(f"Failed to parse JSON response: {e}")
                return {'success': False, 'error': 'Failed to parse API response'}
            
            # Check for success in API response
            if response.status_code == 200:
                # Check for success indicators in the response
                if isinstance(response_data, dict):
                    # Look for common success patterns
                    if response_data.get('success') is True or response_data.get('status') == 'success':
                        logger.info(f"Registration successful for username: {username}")
                        return {
                            'success': True,
                            'username': username,
                            'password': password,
                            'email': email,
                            'parent_id': parent_id,
                            'response': response_data,
                            'cookies': self.session.cookies.get_dict()
                        }
                    elif response_data.get('error') or response_data.get('message'):
                        error_msg = response_data.get('error') or response_data.get('message')
                        logger.warning(f"Registration failed: {error_msg}")
                        return {'success': False, 'error': error_msg}
                
                    # If response is not a dict or doesn't have clear success/error indicators
                    logger.info("Registration completed (API returned 200 OK)")
                    return {
                        'success': True,
                        'username': username,
                        'password': password,
                        'email': email,
                        'parent_id': parent_id,
                        'response': response_data,
                        'cookies': self.session.cookies.get_dict()
                    }
                else:
                    logger.error(f"Registration failed with status code: {response.status_code}")
                    return {'success': False, 'error': f'Registration failed with status code {response.status_code}'}
            else:
                logger.error(f"Registration failed with status code: {response.status_code}")
                return {'success': False, 'error': f'Registration failed with status code {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Unexpected error during registration: {e}", exc_info=True)
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}

async def ichancy(update: Update, context: CallbackContext) -> None:

    logger.info(f"User Click on Ichancy Option")

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("إنشاء حساب جديد", callback_data='create_account')
        ],
        [
            InlineKeyboardButton("سحب من الحساب", callback_data='start'),
            InlineKeyboardButton("شحن حساب", callback_data='start')
        ],
        [InlineKeyboardButton("القائمة الرئيسية", callback_data='start')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text('اختر الخيار المطلوب:', reply_markup=reply_markup)

# Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""

    user_id = str(update.effective_user.id)
    username = update.effective_user.username or update.effective_user.first_name
    store.insertNewUser(user_id , username)
    
    logger.info(f"User {username} ({user_id}) started the bot")
    
    keyboard = [
        [InlineKeyboardButton("🆕 Ichancy", callback_data='ichancy')],
        [InlineKeyboardButton("📊 Check Account Status", callback_data='check_status')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"👋 Welcome to iChancy Account Manager, {username}!\n\n"
        "🤖 I can help you:\n"
        "• Create new iChancy accounts\n"
        "• Check account status\n\n"
        "⚠️ **Disclaimer**: This bot is for educational purposes only. "
        "Please ensure you comply with iChancy's terms of service.\n\n"
        "What would you like to do?"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Balance command handler"""
    user_id = str(update.effective_user.id)
    user = store.getUserByTelegramId(user_id)
    if not user:
        await update.message.reply_text("You don't have any account.")
        return

    await update.message.reply_text(f"Your balance is {user.get('balance', 0)}\nYour telegram id is {user.get('telegram_id', 'N/A')}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button presses"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(update.effective_user.id)
    data = query.data
    
    if data == 'create_account':
        await handle_create_account(query, user_id)
    if data == 'check_status':
        await handle_check_status(query, user_id)
    elif data == 'help':
        await handle_help(query)
    elif data == 'back_to_menu':
        await handle_back_to_menu(query)

async def handle_create_account(update: Update ,context: ContextTypes.DEFAULT_TYPE):
    """Handle account creation"""
    try:
        query = context.user_data.get('query')
        user_id = user_id = str(update.effective_user.id)
        email=context.user_data.get('email')
        username=context.user_data.get('username') 
        password=context.user_data.get('password')
        api = iChancyAPI()
        logger.info(api.COOKIES)
        result = api.register_account(email=email, username=username, password=password)
        
        if result['success']:

            store.insertUserDetailes(telegram_id = user_id,name = username,password=password,email=email)
            keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            success_text = (
                f"✅ **Account Created Successfully!**\n\n"
                f"🆔 **Username**: `{result['username']}`\n"
                f"🔒 **Password**: `{result['password']}`\n"
                f"📧 **Email**: `{result['email']}`\n"
                f"👥 **Parent ID**: `{result.get('parent_id', 'N/A')}`\n\n"
                "⚠️ **Please save these credentials safely!**\n"
                "The account is now created and ready to use."
            )
            
            await update.message.reply_text(success_text)
        else:
            keyboard = [[InlineKeyboardButton("🔄 Try Again", callback_data='create_account'),
                        InlineKeyboardButton("🏠 Menu", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Clean error message for Telegram
            error_msg = result['error']
            # Remove or escape special characters that break Markdown
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
    context.user_data.pop('username', None)
    context.user_data.pop('password', None)
    context.user_data.pop('email', None)

async def handle_back_to_menu(query):
    """Return to main menu"""
    keyboard = [
        [InlineKeyboardButton("🆕 Create New Account", callback_data='create_account')],
        [InlineKeyboardButton("📊 Check Account Status", callback_data='check_status')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🏠 **Main Menu**\n\nWhat would you like to do?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_check_status(query, user_id):
    """Check account status"""
    
    user = store.getUserById(user_id)

    if not user:
        keyboard = [[InlineKeyboardButton("🆕 Create Account", callback_data='create_account'),
                    InlineKeyboardButton("🏠 Menu", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "❌ **No Account Yet**\n\n"
            "You don't have any account.\n"
            "Please create a new account first.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user['created_at']))
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    status_text = (
        "📊 **Account Status**\n\n"
        f"👤 **Username**: `{user['username']}`\n"
        f"📧 **Email**: `{user['email']}`\n"
        f"📅 **Created**: {created_time}\n"
        f"🔗 **Status**: Active"
    )
    
    await query.edit_message_text(status_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_help(query):
    """Show help information"""
    keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    help_text = (
        "❓ **Help & Information**\n\n"
        "🤖 **Bot Commands:**\n"
        "• `/start` - Start the bot and show main menu\n\n"
        "🔧 **Features:**\n"
        "• Create new iChancy accounts automatically\n"
        "• Check account status\n"
        "• Account management (saves your account info)\n\n"
        "⚠️ **Important Notes:**\n"
        "• This bot is for educational purposes\n"
        "• Respect iChancy's terms of service\n"
        "• Keep your credentials secure\n\n"
        "🔧 **How it works:**\n"
        "1. Click 'Create New Account'\n"
        "2. Bot generates random credentials\n"
        "3. Submits registration to iChancy\n"
        "4. Saves account info for you"
    )
    
    await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    try:
        if update and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ **An error occurred**\n\nPlease try again later or contact support.",
                parse_mode='Markdown'
            )
    except Exception:
        logger.error("Failed to send error message to user")

##############################################################
USERNAME, PASSWORD, EMAIL = range(3)



# معالجة الضغط على الزر الداخلي
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'create_account':
        await query.edit_message_text(
            text="Enter User name"
        )
        return USERNAME

    return ConversationHandler.END

# استقبال اسم المستخدم
async def get_username(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    username = update.message.text
    context.user_data['username'] = username
    logger.info("User %s chose username: %s", user.first_name, username)
    
    await update.message.reply_text(
        f"Enter Password"
    )
    return PASSWORD

# استقبال كلمة المرور
async def get_password(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    password = update.message.text
    context.user_data['password'] = password
    logger.info("User %s set password: %s", user.first_name, password)
    username = context.user_data.get('username', 'غير محدد')
    await update.message.reply_text("Enter Email")
    return EMAIL

# استقبال الإيميل وإنهاء العملية
async def get_email(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    email = update.message.text
    context.user_data['email'] = email
    logger.info("User %s provided email: %s", user.first_name, email)
    
    # جمع البيانات
    username = context.user_data.get('username', 'غير محدد')
    password = context.user_data.get('password', 'غير محدد')
    telegram_id = update.effective_user.id
    asyncio.create_task(handle_create_account(update , context=context))


    
    
    return ConversationHandler.END

# إلغاء المحادثة
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        'تم إلغاء عملية إنشاء الحساب.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
##############################################################
def main() -> None:
    """Main function to start the bot"""
    try:
        # Set cookies from the provided cookie string
        
        iChancyAPI.set_cookies_from_string(COOKIE_STRING)
        
        # Create application
        application = Application.builder().token(TOKEN).build()
        # Add conversations
        conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern='^create_account$')],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
        # Add handlers
        application.add_handler(conv_handler)
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('balance', balance))
        application.add_handler(CallbackQueryHandler(ichancy))
        application.add_handler(CallbackQueryHandler(button))
        application.add_error_handler(error_handler)

        # Start the bot
        logger.info("Starting iChancy Account Manager Bot...")
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        application.run_polling(
            poll_interval=2.0,
            timeout=30,
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
    finally:
        logger.info("Bot shutdown complete")

if __name__ == '__main__':
    import sys
    
    logger.info("Initializing iChancy Account Manager Bot...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
