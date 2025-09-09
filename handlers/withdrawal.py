import Logger
import store
from iChancyAPI import iChancyAPI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logger = Logger.getLogger()

def getKeyboard(user_id):
        keyboard = [
            [
                InlineKeyboardButton("Bemo", callback_data='bemo_withdrawal'),
                InlineKeyboardButton("Syriatel Cash 🟢", callback_data='syriatel_cash_withdrawal')
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
        
def getReplyMarkup(user_id):
     keyboard = getKeyboard(user_id)
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def getUserInfoText(user_id):
     user = store.getUserByTelegramId(telegram_id=user_id)
     user_info = 'اختر احد الطرق'
     return user_info
async def handle_withdrawal(query , user_id) -> None:
    logger.info(f"User Click on Withdrawal Option")
    await query.answer()
    await query.edit_message_text(getUserInfoText(user_id), reply_markup=getReplyMarkup(user_id))


