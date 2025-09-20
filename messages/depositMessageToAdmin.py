from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.telegram import ADMIN_ID
def deposit_message(transfeer_id ,provider_type ,telegram_id , telegram_username ,value , transfeer_date ,transaction_id):
    return {'text':reply_text(transfeer_id ,provider_type ,telegram_id , telegram_username ,value , transfeer_date),'parse_mode':parse_mode(), 'reply_markup':reply_markup(transaction_id),'chat_id':chat_id()}

def getKeyboard(transaction_id):
        keyboard = [
            [
                InlineKeyboardButton("تعديل القيمة" , callback_data=f"edit_deposit {transaction_id}")
            ],
            [
                InlineKeyboardButton("تأكيد", callback_data=f"approve_deposit {transaction_id}"),
                InlineKeyboardButton("رفض", callback_data=f"reject {transaction_id}"),
            ]
                ]

        return keyboard
def parse_mode():
      return 'HTML'   

def chat_id():
      return ADMIN_ID
def reply_markup(transaction_id):
     keyboard = getKeyboard(transaction_id)
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(transfeer_id ,provider_type ,telegram_id , telegram_username ,value , transfeer_date):

      text =  f"""
        🆕 :طلب شحن جديد
        🆔 رقم الطلب: #{transfeer_id}
        📌 طريقة التحويل: {provider_type}
        👤 العضو: <a href="tg://user?id={telegram_id}">{telegram_username}</a>
        💰 المبلغ: {value} SYP
        📅 تاريخ الإنشاء: {transfeer_date}
        """
      return text