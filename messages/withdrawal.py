import Logger
import store
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logger = Logger.getLogger()



def withdrawal_message(user_id):
    return reply_text(user_id), reply_markup(user_id)



def getKeyboard():
    keyboard = [
        [
            InlineKeyboardButton("Syriatel Cash 🟢", callback_data='syriatel_cash_withdrawal'),
            InlineKeyboardButton("Bemo", callback_data='bemo_withdrawal'),
        ],
        [
            InlineKeyboardButton("Payeer", callback_data='payeer_withdrawal'),
            InlineKeyboardButton("حوالة", callback_data='hawala_withdrawal')
        ],
        [
            InlineKeyboardButton("Sham Cash (SYP) 🇸🇾", callback_data='sham_cash_syp_withdrawal')
        ],
        [
            InlineKeyboardButton("Sham Cash (USD) 💲", callback_data='sham_cash_usd_withdrawal')
        ],
        [
            InlineKeyboardButton("Coinex", callback_data='coinex_withdrawal'),
            InlineKeyboardButton("Cwallet", callback_data='cwallet_withdrawal')
        ],
        [
            InlineKeyboardButton("USDT Bep 20", callback_data='usdt_bep_20_withdrawal'),
            InlineKeyboardButton("USDT trc 20", callback_data='usdt_trc_20_withdrawal')
        ],
        [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_menu')],
    ]

    return keyboard
        
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(user_id):
     user = store.getUserByTelegramId(telegram_id=user_id)
     user_info = 'اختر احد الطرق'
     return user_info