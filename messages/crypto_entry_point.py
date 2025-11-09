import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logger = Logger.getLogger()



def crypto_entry_point_message(DAMUSDT):
    return reply_text(DAMUSDT), reply_markup()



def getKeyboard():
    keyboard = [
                    [
                            InlineKeyboardButton('USDT-TRC20' , callback_data = "USDT-TRC20"),
                    ],
                    [
                            InlineKeyboardButton('USDT-BEP20' , callback_data = "USDT-BEP20"),
                    ],
                    [  
                            InlineKeyboardButton('القائمة الرئيسية', callback_data = "back_to_menu")
                    ]
                        
                ]

    logger.info("we got alog message")
    return keyboard
        
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(DAMUSDT):
    text = f"1 USDT = {DAMUSDT}"
    
    return text