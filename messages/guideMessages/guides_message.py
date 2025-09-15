


from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def guides_message(query):
    return reply_text() , reply_markup(query)


def getKeyboard(query):
    keyboard = [[InlineKeyboardButton("ما هو موقع Ichancy ؟", callback_data='guides_what_is_ichancy')],
                [InlineKeyboardButton("كيفية شحن الرصيد ضمن بوت Ichancy", callback_data='guides_how_deposit_telegram_account')],
                [InlineKeyboardButton("كيفية إنشاء حساب Ichancy جديد", callback_data='guides_how_to_create_new_account')],
                [InlineKeyboardButton("كيفية سحب الرصيد من بوت Ichancy", callback_data='guides_how_withdraw_telegram_account')],
                [InlineKeyboardButton("كيفية شحن رصيد ضمن حساب Ichancy", callback_data='guides_how_deposit_ichancy_account')],
                [InlineKeyboardButton("كيفية سحب رصيد من حساب Ichancy", callback_data='guides_how_withdraw_ichancy_account')],
                [InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')],]
    return keyboard

def reply_markup(query):
    keyboard = getKeyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def reply_text():
    text = 'الشروحات'

    return text