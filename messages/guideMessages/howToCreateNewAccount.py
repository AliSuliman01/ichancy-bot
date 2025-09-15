from telegram import  InlineKeyboardButton, InlineKeyboardMarkup

async def how_to_create_new_account():
    return reply_text(),reply_markup()


def getKeyboard():
        keyboard = [[InlineKeyboardButton("رجوع للشروحات", callback_data='guides')]]
        return keyboard


def reply_markup():
    keyboard = getKeyboard()
    return InlineKeyboardMarkup(keyboard)


def reply_text():
    text = """كيفية إنشاء حساب Ichancy جديد

    لإنشاء حساب جديد على موقع Ichancy عبر البوت، يرجى اتباع الخطوات التالية:

    1. اضغط على خيار "Ichancy" في واجهة البوت.

    2. اختر "حساب Ichancy جديد".

    3. أدخل اسمًا للحساب الجديد.

    4. أدخل كلمة مرور لا تقل عن 8 أرقام.

    5. أدخل المبلغ الذي ترغب بشحن الحساب به بالدولار ($).

    6. انتظر حوالي 15 ثانية لمعالجة الطلب.

    ✅ تم إنشاء الحساب بنجاح."""

    return text