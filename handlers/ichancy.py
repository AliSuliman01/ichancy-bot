import Logger
import store
from iChancyAPI import iChancyAPI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logger = Logger.getLogger()

def getKeyboard(user_id):
        keyboard = [
            [
                InlineKeyboardButton("سحب من الحساب", callback_data='start'),
                InlineKeyboardButton("شحن حساب", callback_data='start')
            ],
            [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_menu')],
        ]
        if not  store.getUserByTelegramId(telegram_id=user_id).get('name'):
            keyboard = [
            [
                InlineKeyboardButton("إنشاء حساب جديد", callback_data='create_account')
            ],
            [
                InlineKeyboardButton("سحب من الحساب", callback_data='start'),
                InlineKeyboardButton("شحن حساب", callback_data='start')
            ],
            [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_menu')],
        ]

        return keyboard
        
def getReplyMarkup(user_id):
     keyboard = getKeyboard(user_id)
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def getUserInfoText(user_id):
     user = store.getUserByTelegramId(telegram_id=user_id)
     user_info = 'اختر الخيار الذي تريده'

     if user.get('name'):
        user_info = (
                       "https://www.ichancy.com/ar \n\n"
                       f"👤 الدخول: {user['name']}\n"
                       f"📧 الإيميل: {user['email']}\n"
                       f"🔒 كلمة السر: {user['password']} "
                )
        
     return user_info
async def handle_ichancy(query , user_id) -> None:
    logger.info(f"User Click on Ichancy Option")
    await query.answer()

    await query.edit_message_text(getUserInfoText(user_id), reply_markup=getReplyMarkup(user_id))


