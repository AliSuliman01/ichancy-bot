from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.telegram import ADMIN_ID
def withdraw_message(transfeer_id ,provider_type ,telegram_id , telegram_username ,value , transfeer_date ,transaction_id , TAX , withdraw_number):
    return {'text':reply_text(transfeer_id ,provider_type ,telegram_id , telegram_username ,value , transfeer_date , TAX,withdraw_number),'parse_mode':parse_mode(), 'reply_markup':reply_markup(transaction_id ,TAX),'chat_id':chat_id()}

def getKeyboard(transaction_id , TAX):
        keyboard = [
            [
                InlineKeyboardButton("تعديل القيمة" , callback_data=f"edit_withdraw {transaction_id} {TAX}")
            ],
            [
                InlineKeyboardButton("تأكيد", callback_data=f"approve_withdraw {transaction_id}"),
                InlineKeyboardButton("رفض", callback_data=f"reject {transaction_id}"),
            ]
                ]

        return keyboard
def parse_mode():
      return 'HTML'   

def chat_id():
      return ADMIN_ID
def reply_markup(transaction_id , TAX):
     keyboard = getKeyboard(transaction_id ,TAX)
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(transfeer_id ,provider_type ,telegram_id , telegram_username ,value , transfeer_date ,TAX,withdraw_number):

      text =  f"""
        🆕 :طلب سحب جديد
        🆔 رقم الطلب: #{transfeer_id}
        📌 طريقة التحويل: {provider_type}
        📌 الرقم: {withdraw_number}
        👤 العضو: <a href="tg://user?id={telegram_id}">{telegram_username}</a>
        💰المبلغ: {value}
        💰النسبة المئوية للاقتطاع: {TAX*100}%
        💰المبلغ المقتطع: {value*TAX}
        💰 المبلغ المستحق بعد الاقتطاع: {value - value*TAX} SYP
        📅 تاريخ الإنشاء: {transfeer_date}
        """
      return text