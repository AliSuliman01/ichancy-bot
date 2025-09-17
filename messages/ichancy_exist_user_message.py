from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from models.user import User
# import validations.ichancy
def ichancy_message(user):
    return reply_text(user), reply_markup()


def getKeyboard():
    keyboard = [
        [
            InlineKeyboardButton("سحب من الحساب", callback_data='withdrawal_account'),
            InlineKeyboardButton("شحن حساب", callback_data='deposit_account')
        ],
        [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_menu')],
    ]

    return keyboard
        
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(user):
    user_info = (
        "https://www.ichancy.com/ar \n\n"
        f"👤 الدخول: {user['name']}\n"
        f"📧 الإيميل: {user['email']}\n"
        f"🔒 كلمة السر: {user['password']} "
    )
    return user_info
        
