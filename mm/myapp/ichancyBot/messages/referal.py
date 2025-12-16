import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.telegram import BOT_NAME
logger = Logger.getLogger()



def referal_message(num_of_referal_child,referal_code,date_of_distribution_referals):
    # logger.info("get referal message")
    return reply_text(num_of_referal_child,referal_code,date_of_distribution_referals), reply_markup()



def getKeyboard():

    keyboard = [[InlineKeyboardButton("التفاصيل", callback_data = "referal_details")],
                [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_menu')]
                ]
    # logger.info("get referal key board")
    return keyboard
        
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     # logger.info("get referal mark up")
     return reply_markup

def reply_text(num_of_referal_child,referal_code,date_of_distribution_referals):
    text = f"""نظام احالات Ichancy Gilbert
    يقدّم لك فرصة لدخل إضافي كل 10 أيام .
    كن وكيلاً معنا بأبسط طريقة
    إحصل على نسبة ثابتة لكل عمليات الشحن والتعبئة القادمة عن طريق رابط احالتك ضمن البوت 
    .....
    1-عند الدخول الى البوت قم بنسخ رابط الاحالة الخاص بك عن طريق الضغط على خيار رابط الاحالة الخاص بي
    2- عندما تقوم بنشر رابط احالتك ويقوم أحد بالتسجيل عن طريقة سنبدأ بحساب نسبة ثابتة لجميع عمليات السحب والتعبئة عن طريقك . 
    3- يتم حساب الارباح عند وجود 3 إحالات نشطة او أكثر
    ماذا تنتظر...! 
    توزيع النسب كل 10 أيام

    عدد الاحالات التابعة لك: {num_of_referal_child}
    رابط الإحالة الخاص بك: 
    http://t.me/{BOT_NAME}?start={referal_code}

    الموعد القادم لتوزيع الاحالات: 
    {date_of_distribution_referals}
    """ 
    
    return text