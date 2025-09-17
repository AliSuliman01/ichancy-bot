from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def deposit_message():
    return reply_text(), reply_markup()

def getKeyboard():
        keyboard = [
            [
                InlineKeyboardButton("Syriatel Cash 🟢", callback_data='syriatel_cash_deposit'),
                InlineKeyboardButton("Bemo", callback_data='bemo_deposit'),
            ],
            [
                InlineKeyboardButton("Payeer", callback_data='payeer_deposit'),
            ],
            [
                InlineKeyboardButton("عملات ومحافظ رقمية (USDT)", callback_data='crypto_deposit')
            ],
            [
                InlineKeyboardButton("Sham Cash Auto ⚡️ (USD, SYP)", callback_data='sham_cash_auto_deposit')
            ],
            [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_menu')],
        ]

        return keyboard
        
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text():
     user_info = 'اختر احد الطرق'
     return user_info