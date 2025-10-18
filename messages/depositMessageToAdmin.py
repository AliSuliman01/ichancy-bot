from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.telegram import ADMIN_ID
def deposit_message(transfeer_id ,provider_type ,telegram_id , telegram_username ,value , transfeer_date ,transaction_id , transfeer_num , text ,currency = 'SYP'):
    return {'text':reply_text(transfeer_id ,provider_type ,telegram_id , telegram_username ,value , transfeer_date , transfeer_num ,text),'parse_mode':parse_mode(), 'reply_markup':reply_markup(transaction_id ,currency,value),'chat_id':chat_id()}

def getKeyboard(transaction_id , currency , value):
        keyboard = [
            [
                InlineKeyboardButton("تعديل القيمة" , callback_data=f"edit_deposit {transaction_id} {currency} {value}")
            ],
            [
                InlineKeyboardButton("تأكيد", callback_data=f"approve_deposit {transaction_id} {currency}  {value}"),
                InlineKeyboardButton("رفض", callback_data=f"reject {transaction_id} {currency}  {value}"),
            ]
                ]

        return keyboard
def parse_mode():
      return 'HTML'   

def chat_id():
      return ADMIN_ID
def reply_markup(transaction_id , currency , value):
     keyboard = getKeyboard(transaction_id , currency , value)
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(transfeer_id ,provider_type ,telegram_id , telegram_username ,value , transfeer_date , transfeer_num , text):

    #   text =  f"""
    #     🆕 :طلب شحن جديد
    #     🆔 رقم الطلب: #{transfeer_id}
    #     📌 طريقة التحويل: {provider_type}.
    #     👤 العضو: <a href="tg://user?id={telegram_id}">{telegram_username}</a>
    #     🆔 الكود: {transfeer_num}
    #     💰 المبلغ: {value} SYP
    #     📅 تاريخ الإنشاء: {transfeer_date}
    #     """
    #    return text
      text =text.replace("تم استلام طلبك وسيتم إعلامك عند معالجته\n" , "")
      return text
     