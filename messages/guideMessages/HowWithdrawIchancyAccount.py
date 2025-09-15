from telegram import  InlineKeyboardButton, InlineKeyboardMarkup

async def how_withdrawal_ichancy_account():
    return reply_text(),reply_markup()


def getKeyboard():
        keyboard = [[InlineKeyboardButton("رجوع للشروحات", callback_data='guides')]]
        return keyboard


def reply_markup():
    keyboard = getKeyboard()
    return InlineKeyboardMarkup(keyboard)


def reply_text():
    text = """كيفية سحب رصيد من حساب Ichancy

    لسحب رصيد من حسابك في موقع Ichancy عبر البوت، يرجى اتباع الخطوات التالية:

    1. اضغط على خيار "Ichancy" في واجهة البوت.

    2. اختر "سحب رصيد من حساب Ichancy".

    3. أدخل معرّف الحساب أو اسم حساب Ichancy الذي ترغب بالسحب منه.

    4. أدخل المبلغ المطلوب سحبه بالدولار ($).

    5. انتظر حوالي 15 ثانية حتى تتم معالجة العملية.

    ✅ تم سحب الرصيد بنجاح."""

    return text