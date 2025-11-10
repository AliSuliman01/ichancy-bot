import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logger = Logger.getLogger()



def term_message():
    return reply_text(), reply_markup()



def getKeyboard():
    keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu' ,)]]

    return keyboard
        
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text():
    
    term_text = (
"عند الضغط على زر موافقة فأنت توافق على الشروط القائمة ضمن البوت ويحق لك الإعتراض في حال مواجهة أي مشكلة خارجة عن شروط وقوانين البوتيرجى قراءة هذه الشّروط قبل استخدام البوت لضمان تجربة آمنة وسلسة:\n\n"

"البوت مخصّص لإنشاء الحسابات، والسّحب، والتعبئة الفورية لحسابات موقع Ichancy.\n\n"

"1_منع الحسابات المتعدّدة:\n"
"إنشاء أكثر من حساب للشّخص الواحد مخالف للقوانين، وقد يؤدّي إلى حظر الحسابات المرتبطة وتجميد أرصدتها، وذلك بناءاً على سياسة اللّعب النظيف .\n\n"
"2_تبديل طرق الدفع غير مسموح:\n"
"لا يُسمح بشحن رصيد وسحبه بغرض التبديل بين وسائل الدفع المختلفة. في حال اكتشاف عملية كهذه، يتم سحب الرّصيد والتّحفظ عليه دون إشعار مسبق.\n\n"
"3_شروط أرباح الإحالات:\n"
"تُحتسب أرباح الإحالة فقط بعد تسجيل 3 إحالات نشطة أو أكثر (أي قاموا بالتعبئة الفعلية).\n\n\n\n"
"⛔️تنبيه:\n"
"أي محاولة للتّحايل أو مخالفة الشروط ستؤدي إلى إيقاف الحساب وتجميد الأرصدة.\n"
)
    return term_text