from telegram import  InlineKeyboardButton, InlineKeyboardMarkup

async def how_deposit_telegram_account_message():
    return reply_text(),reply_markup()


def getKeyboard():
        keyboard = [[InlineKeyboardButton("رجوع للشروحات", callback_data='guides')]]
        return keyboard


def reply_markup():
    keyboard = getKeyboard()
    return InlineKeyboardMarkup(keyboard)


def reply_text():
    text = """كيفية شحن الرصيد ضمن بوت Ichancy

    يرجى اتباع الخطوات التالية لإتمام عملية شحن الرصيد بنجاح:

    1. اضغط على خيار "شحن رصيد" في واجهة البوت.

    2. اختر طريقة الدفع المناسبة لك من بين الخيارات المتاحة.

    3. قم بإرسال المبلغ الذي ترغب في شحنه إلى العنوان المخصّص (أقل مبلغ يمكن شحنه هو 1 دولار أمريكي).

    4. بعد إتمام التحويل، أدخل كود عملية التحويل، ثم أدخل قيمة المبلغ المرسل.

    ✅ تم شحن البوت بنجاح."""   

    return text