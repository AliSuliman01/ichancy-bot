import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logger = Logger.getLogger()



def contact_us_message():
    return reply_text(), reply_markup()



def getKeyboard():
    keyboard = [[InlineKeyboardButton('مشكلة تقنية ضمن البوت' , callback_data = "problem_in_bot")],
                [InlineKeyboardButton('مشكلة تقنية ضمن الموقع' , callback_data = "problem_in_website")],
                [InlineKeyboardButton('القائمة الرئيسية', callback_data = "back_to_menu")]
                ]

    return keyboard
        
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text():
    text = "الدعم"
    
    return text