import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logger = Logger.getLogger()



def money_order_withdrawal_entry_point_message():
    return reply_text(), reply_markup()



def getKeyboard():
    keyboard = [
                    [
                        InlineKeyboardButton('القدموس' , callback_data = "qadmous"),
                        InlineKeyboardButton('الهرم' , callback_data = "haram"),
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
    text = "اختر شركة الشحن"
    
    return text