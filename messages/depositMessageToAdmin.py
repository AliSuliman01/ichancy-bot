from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.telegram import ADMIN_ID
def deposit_message(transfeer_id ,transfeer_function ,telegram_id , telegram_username ,value , transfeer_date):
    return {'text':reply_text(transfeer_id ,transfeer_function ,telegram_id , telegram_username ,value , transfeer_date),'parse_mode':parse_mode(), 'reply_markup':reply_markup(),'chat_id':chat_id()}

def getKeyboard():
        keyboard = [
            [
                InlineKeyboardButton("تعديل القيمة" , callback_data="edit_value")
            ],
            [
                InlineKeyboardButton("تأكيد", callback_data='approve'),
                InlineKeyboardButton("رفض", callback_data='reject'),
            ]
                ]

        return keyboard
def parse_mode():
      return 'HTML'   

def chat_id():
      return ADMIN_ID
def reply_markup():
     keyboard = getKeyboard()
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(transfeer_id ,transfeer_function ,telegram_id , telegram_username ,value , transfeer_date):
      text =  f"""
        🆕 :طلب شحن جديد
        🆔 رقم الطلب: #{transfeer_id}
        📌 طريقة التحويل: {transfeer_function}
        👤 العضو: <a href="tg://user?id={telegram_id}">{telegram_username}</a>
        💰 المبلغ: {value} SYP
        📅 تاريخ الإنشاء: {transfeer_date}
        """
      return text