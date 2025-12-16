import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.telegram import BOT_NAME
logger = Logger.getLogger()



def referal_message(num_of_activate_referal_child,referal_code,date_of_distribution_referals,value):
    # logger.info("get referal details message")
    return reply_text(num_of_activate_referal_child,referal_code,date_of_distribution_referals,value), reply_markup()



def getKeyboard():

    keyboard = [[InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_menu')]]
    # logger.info("get referal details key board")
    return keyboard
        
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     # logger.info("get referal details mark up")
     return reply_markup

def reply_text(num_of_activate_referal_child,referal_code,date_of_distribution_referals,value):
    text = f"""Ichancy Gilbert
    
    عدد الاحالات النشطة في هذه الدورة: {num_of_activate_referal_child}
    القيمة الاجمالية للدخل من الإحالات: {value}

    رابط الإحالة الخاص بك: 
    http://t.me/{BOT_NAME}?start={referal_code}

    الموعد القادم لتوزيع الاحالات: 
    {date_of_distribution_referals}
    """ 
    
    return text