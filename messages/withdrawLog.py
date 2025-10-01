import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logger = Logger.getLogger()
texts = []


def withdraw_log_message(transactions , page):
    return reply_text(transactions , page), reply_markup(page)



def getKeyboard(page):
    global texts
    if len(texts)>page+1:
            print(len(texts))
            keyboard = [    
                            [InlineKeyboardButton('الصفحة التالية', callback_data = f"withdraw_log {page}") ],
                            [   InlineKeyboardButton('القائمة الرئيسية', callback_data = "back_to_menu")],
                    ]
    else:
        keyboard= [[InlineKeyboardButton('القائمة الرئيسية', callback_data = "back_to_menu")]]

    logger.info("we got deposit log message")
    return keyboard
        
def reply_markup(page):
     keyboard = getKeyboard(page)
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(transactions , page):
    text  = ""
    global texts
    texts=[]
    for transaction in transactions:
        provider_type = transaction.get('provider_type')
        value = transaction.get('value')
        status = transaction.get('status')
        created_at = transaction.get('created_at').date()
        text =(f"الطريقة: {provider_type}  \n"
                f"القيمة: {-value}\n"
                f"الحالة: {status}\n"
                f"تاريخ العملية : {created_at}\n"
                "----------------------------------------\n")+text
        if len(text)>500:
            texts.append(text)
            text=""
    if len(text)>0:
        texts.append(text)
    if len(texts)>0:
        return texts[page] 
    else: 
        return "\nلا يوجد عمليات سحب\n"

