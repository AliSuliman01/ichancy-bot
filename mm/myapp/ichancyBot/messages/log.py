import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logger = Logger.getLogger()



def log_message():
    return reply_text(), reply_markup()



def getKeyboard():
    keyboard = [
                    [
                        InlineKeyboardButton('سجل الشحن' , callback_data = "deposit_log"),
                        InlineKeyboardButton('سجل السحب' , callback_data = "withdraw_log"),
                    ],
                    [   InlineKeyboardButton('القائمة الرئيسية', callback_data = "back_to_menu")
                     ]
                        
                ]

    # logger.info("we got alog message")
    return keyboard
        
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text():
    text = "السجل"
    
    return text