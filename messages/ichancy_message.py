import store
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import helpers

def ichancy_message(user_id):
    return reply_text(user_id), reply_markup(user_id)


def getKeyboard(user_id):
        keyboard = [
            [
                InlineKeyboardButton("سحب من الحساب", callback_data='withdrawal_account'),
                InlineKeyboardButton("شحن حساب", callback_data='deposit_account')
            ],
            [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_menu')],
        ]
        if not  store.getUserByTelegramId(telegram_id=user_id).get('name'):
            keyboard = [
            [
                InlineKeyboardButton("إنشاء حساب جديد", callback_data='create_account')
            ],
            *keyboard
        ]

        return keyboard
        
def reply_markup(user_id):
     keyboard = getKeyboard(user_id)
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(user_id):
     user = store.getUserByTelegramId(telegram_id=user_id)
     user_info = 'اختر الخيار الذي تريده'

     if user and user.get('name'):
        user_info = helpers.getStatusText(user)
        
     return user_info