from telegram import  InlineKeyboardButton, InlineKeyboardMarkup

def how_deposit_ichancy_account_message():
    return reply_text(),reply_markup()


def getKeyboard():
        keyboard = [[InlineKeyboardButton("رجوع للشروحات", callback_data='guides')]]
        return keyboard


def reply_markup():
    keyboard = getKeyboard()
    return InlineKeyboardMarkup(keyboard)


def reply_text():
    text = """كيفية شحن رصيد ضمن حساب Ichancy
    لشحن رصيد إلى حسابك في موقع Ichancy عبر البوت، يرجى اتباع الخطوات التالية:

    1. اضغط على خيار "Ichancy" في واجهة البوت.

    2. اختر "شحن حساب Ichancy".

    3. أدخل معرّف الحساب أو اسم حساب Ichancy الذي ترغب بشحنه.

    4. أدخل المبلغ المطلوب شحنه بالليرة السوريّة .

    5. انتظر حوالي 15 ثانية حتى تتم معالجة العملية.

    ✅ تم شحن الحساب بنجاح."""

    return text