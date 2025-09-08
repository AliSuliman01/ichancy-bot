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
import cloudscraper
import store

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7985162765:AAEg_aQ-cLRMxLVzAeTwu7_EIgn81THL_BM')
SESSION_FILE = 'ichancy_sessions.json'
COOKIE_STRING = 'PHPSESSID_3a07edcde6f57a008f3251235df79776a424dd7623e40d4250e37e4f1f15fadf=bd652b7e6716d615eba9080694540023; languageCode=en_GB; language=English%20%28UK%29; __cf_bm=D6vWouVdssX.jKB6m1GRE_Cjpp1S2KAJi2WYB8fkFtg-1757271805-1.0.1.1-F9NumzrHfKvsGtIBYu_D_gp5imgdee0J5dBUpsKK9GAGFhLhpikmFrt0TWRma6hup.SMV3tcXH9bCFMEtmTqtUJSBTdXfeA5E_kd2yDO_mM; cf_clearance=IdBzv2tO4J86QVdliVbVlmKeHg2WNqd2iSsLutK51BE-1757272423-1.2.1.1-THo5gpgoAJXXPqn0_nNNJ._1HDnpMq3rEfGE6ggf0YjfEXNaKhgdxtvXgt5tzwI4Zf7W0_gFFbNaZ9ismBMhP.bj3EHGlV47UzSBefd0dke42vtwGd_i53un4dPAtP.zoRJ9tSGXmW87tC834g.LALYIvZpfKi5FnWPSuI_fOBrIXTvD_hb4Aec2reD30hi50BNK1pWCS0zGUvmT8pHBYmrQz1oJlksXCAbBbZGd_x8'
# Validate bot token


if not TOKEN or TOKEN.startswith('YOUR_BOT_TOKEN'):
    logger.error("Please set TELEGRAM_BOT_TOKEN environment variable")
    exit(1)

class iChancyAPI:
    BASE_URL = 'https://www.ichancy.com'
    
    # Static headers - update these as needed
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',

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
    
    # Static cookies - update these as needed
    COOKIES = {
        # Add your cookies here
        # 'session_id': 'your_session_id',
        #'csrf_token': 'your_csrf_token',إ
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
        # # Try cloudscraper first for better Cloudflare bypass
        try:
            self.session = cloudscraper.create_scraper()
            logger.info("Initialized with cloudscraper for Cloudflare bypass")
        except Exception as e:
            logger.warning(f"Failed to initialize cloudscraper: {e}, falling back to requests")
        self.session = requests.Session()
        
        self.session.headers.update(self.HEADERS)
        self.session.cookies.update(self.COOKIES)
        logger.info("Initialized iChancy API with headers and cookies")
        
    # def generate_random_username(self):
    #     return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    # def generate_random_password(self):
    #     """Generate password meeting the requirements: uppercase, lowercase, numeric, min 8 chars"""
    #     password = [
    #         random.choice(string.ascii_uppercase),  # At least one uppercase
    #         random.choice(string.ascii_lowercase),  # At least one lowercase  
    #         random.choice(string.digits),           # At least one numeric
    #     ]
        
    #     # Fill the rest with random characters (minimum 8 total)
    #     remaining_length = max(5, random.randint(5, 9))  # 8-12 characters total
    #     for _ in range(remaining_length):
    #         password.append(random.choice(string.ascii_letters + string.digits + '!@#$%^&*'))
        
    #     # Shuffle to avoid predictable patterns
    #     random.shuffle(password)
    #     return ''.join(password)
    
    # def generate_random_email(self):
    #     domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com']
    #     return f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@{random.choice(domains)}"
    
    # def generate_random_first_name(self):
    #     """Generate a random first name"""
    #     first_names = ['Ahmed', 'Fatima', 'Omar', 'Layla', 'Hassan', 'Zara', 'Khalid', 'Amira', 'Yusuf', 'Sara']
    #     return random.choice(first_names)
    
    # def generate_random_last_name(self):
    #     """Generate a random last name"""
    #     last_names = ['Al-Ahmad', 'Al-Hassan', 'Al-Omar', 'Al-Zahra', 'Al-Khalil', 'Al-Nouri', 'Al-Mansour', 'Al-Rashid', 'Al-Farid', 'Al-Saeed']
    #     return random.choice(last_names)
    
    def test_api_connection(self):
        """Test if we can access the API endpoint"""
        try:
            # First try to access the main site to establish session
            logger.info("Testing main site access...")
            main_response = self.session.get("https://agents.ichancy.com/", timeout=10)
            logger.info(f"Main site response status: {main_response.status_code}")
            
            # Then test the API endpoint
            test_url = "https://agents.ichancy.com/global/api/Player/registerPlayer"
            headers = self.HEADERS.copy()
            headers.update({
                'Content-Type': 'application/json',
            })
            
            logger.info("Testing API connection...")
            response = self.session.get(test_url, headers=headers, timeout=10)
            logger.info(f"API test response status: {response.status_code}")
            
            # Check for Cloudflare challenge
            if 'cf-mitigated' in response.headers and response.headers['cf-mitigated'] == 'challenge':
                logger.warning("Cloudflare challenge detected in API test")
                return False
            
            return response.status_code != 403
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
            return False
    
    def register_account(self, username=None, password=None, email=None, parent_id="2495754"):
        """
        Register a new account using the iChancy API
        """
        logger.info("Starting account registration process")
        
        try:
            # Test API connection first
            if not self.test_api_connection():
                logger.warning("API connection test failed - this may indicate Cloudflare protection or expired cookies")
                # Continue anyway but warn the user
            
            # Generate random credentials if not provided
            username = username #or self.generate_random_username()
            password = password #or self.generate_random_password()
            email = email #or self.generate_random_email()
            
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
            
            # Update headers for JSON API
            headers = self.HEADERS.copy()
            headers.update({
                'Content-Type': 'application/json',
            })
            
            # Log the request details for debugging
            logger.info(f"Making request to: {register_url}")
            logger.info(f"Headers: {headers}")
            logger.info(f"Payload: {payload}")
        
            # Submit registration
            logger.info("Submitting registration to API")
            try:
                response = self.session.post(
                    register_url, 
                    json=payload, 
                    headers=headers,
                    timeout=30
                )
                
                # Log response details for debugging
                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Response headers: {dict(response.headers)}")
                logger.info(f"Response text: {response.text[:500]}...")  # First 500 chars
                
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

# Session Management
def load_sessions():
    """Load user sessions from file"""
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading sessions: {e}")
        return {}

def save_sessions(sessions):
    """Save user sessions to file"""
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(sessions, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving sessions: {e}")

# Global session storage
user_sessions = load_sessions()

# Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""

    user_id = str(update.effective_user.id)
    username = update.effective_user.username or update.effective_user.first_name
    store.insertNewUser(user_id , username)
    
    logger.info(f"User {username} ({user_id}) started the bot")
    
    keyboard = [
        [InlineKeyboardButton("🆕 Create New Account", callback_data='create_account')],
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

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button presses"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(update.effective_user.id)
    data = query.data
    
    # if data == 'create_account':
    #     await handle_create_account(query, user_id)
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
            # Store session
            user_sessions[user_id] = {
                'username': result['username'],
                'password': result['password'],
                'email': result['email'],
                'parent_id': result.get('parent_id', 'N/A'),
                'cookies': result['cookies'],
                'created_at': time.time()
            }
            save_sessions(user_sessions)

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
            
            await update.message.reply_text(
                f"❌ **Account Creation Failed**\n\n"
                f"Error: {error_msg}\n\n"
                "You can try again or return to the main menu.",
                
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
    if user_id not in user_sessions:
        keyboard = [[InlineKeyboardButton("🆕 Create Account", callback_data='create_account'),
                    InlineKeyboardButton("🏠 Menu", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "❌ **No Active Session**\n\n"
            "You don't have any saved account sessions.\n"
            "Please create a new account first.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    session = user_sessions[user_id]
    created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session['created_at']))
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    status_text = (
        "📊 **Account Status**\n\n"
        f"👤 **Username**: `{session['username']}`\n"
        f"📧 **Email**: `{session['email']}`\n"
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
        "• Session management (saves your account info)\n\n"
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
        cookie_string = COOKIE_STRING
        iChancyAPI.set_cookies_from_string(cookie_string)
        
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
