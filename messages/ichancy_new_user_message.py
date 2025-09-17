from telegram import InlineKeyboardButton, InlineKeyboardMarkup
def ichancy_message(user_id):
    return reply_text(), reply_markup(user_id)


def getKeyboard(user_id):
        keyboard = [
            [
                InlineKeyboardButton("إنشاء حساب جديد", callback_data='create_account')
            ],
            [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_menu')],
        ]
        
        return keyboard
        
def reply_markup(player_id):
    keyboard = getKeyboard(player_id)
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def reply_text():
    user_info = 'يرجى انشاء حساب اولا لتتمكن من الايداع والسحب'

    return user_info