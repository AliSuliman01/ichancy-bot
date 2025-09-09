import Logger
import store
from iChancyAPI import iChancyAPI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logger = Logger.getLogger()

def getKeyboard(user_id):
        keyboard = [
            [
                InlineKeyboardButton("Bemo", callback_data='bemo_deposit'),
                InlineKeyboardButton("Syriatel Cash 🟢", callback_data='syriatel_cash_deposit')
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
        
def getReplyMarkup(user_id):
     keyboard = getKeyboard(user_id)
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def getUserInfoText(user_id):
     user = store.getUserByTelegramId(telegram_id=user_id)
     user_info = 'اختر احد الطرق'
     return user_info
async def handle_deposit(query , user_id) -> None:
    logger.info(f"User Click on Withdrawal Option")
    await query.answer()
    await query.edit_message_text(getUserInfoText(user_id), reply_markup=getReplyMarkup(user_id))


