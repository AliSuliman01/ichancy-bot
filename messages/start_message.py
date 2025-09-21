from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def start_message():
    return reply_text(), reply_markup()

def reply_text():
    welcome_text = (
            f"أهلا بك في بوت\n "
             "Gilbert Ichancy"
        )
    return welcome_text

def reply_markup():
    return InlineKeyboardMarkup(getKeyboard())

def getKeyboard():
    keyboard = [
        [
            InlineKeyboardButton("⚡️ Ichancy", callback_data='ichancy')
        ],
        [
            InlineKeyboardButton("شحن رصيد 📥", callback_data='deposit'),
            InlineKeyboardButton("سحب رصيد 📤", callback_data='withdrawal'),
        ],
        [
            InlineKeyboardButton("نظام الاحالات 💰", callback_data='referal')
        ],
        [
            InlineKeyboardButton("اهداء رصيد 🎁", callback_data='send_gift'),
            InlineKeyboardButton("كود هدية 🎁", callback_data='reseive_gift'),
        ],
        [
            InlineKeyboardButton("رسالة للادمن 📨", callback_data='admin_message'),
            InlineKeyboardButton("تواصل معنا ✉️", callback_data='contact_us'),
        ],
        [
            InlineKeyboardButton("السجل 📜", callback_data='log'),
            InlineKeyboardButton("الشروحات 📝", callback_data='guides'),
        ],
        [InlineKeyboardButton("الشروط والاحكام 📌", callback_data='terms_and_conditions')],
    ]
    return keyboard
