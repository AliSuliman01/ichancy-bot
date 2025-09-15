from telegram import  InlineKeyboardButton, InlineKeyboardMarkup

async def how_withdrawal_telegram_account():
    return reply_text(),reply_markup()


def getKeyboard():
        keyboard = [[InlineKeyboardButton("رجوع للشروحات", callback_data='guides')]]
        return keyboard


def reply_markup():
    keyboard = getKeyboard()
    return InlineKeyboardMarkup(keyboard)


def reply_text():
    text = """كيفيّة سحب الرصيد من بوت Ichancy

    لإتمام عملية السحب بنجاح، يرجى اتباع الخطوات التالية:

    1. اضغط على خيار "سحب رصيد" من واجهة البوت.

    2. اختر طريقة السحب المناسبة لك من بين الوسائل المتاحة.

    3. أدخل بياناتك المطلوبة بدقة، بحسب الطريقة التي قمت باختيارها.

    4. أدخل المبلغ الذي ترغب بسحبه.

    ✅ تم تنفيذ عملية السحب بنجاح.
    يتم معالجة طلب السحب خلال مدة أقصاها نصف ساعة."""   

    return text