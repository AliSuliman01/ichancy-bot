from telegram import ReplyKeyboardRemove

def message(message , telegram_id):
    return reply_text(message , telegram_id), reply_markup()


def getKeyboard():
    pass

def reply_markup():
    return ReplyKeyboardRemove()

def reply_text(balance , telegram_id):
    text = f"  رصيدك هو : {balance}\nمعرف التلغرام الخاص بك هو :  {telegram_id}"
    return text