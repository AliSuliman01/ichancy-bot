from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.telegram import ADMIN_ID
def withdraw_message(transaction_id , TAX , chat_id ,text):
    return {'text':reply_text(text),'parse_mode':parse_mode(), 'reply_markup':reply_markup(transaction_id ,TAX,chat_id),'chat_id':chat__id(chat_id)}

def getKeyboard(transaction_id , TAX , chat_id):
        keyboard = [
            [
                InlineKeyboardButton("تعديل القيمة" , callback_data=f"edit_withdraw {transaction_id} {TAX} {chat_id}")
            ],
            [
                InlineKeyboardButton("تأكيد", callback_data=f"approve_withdraw {transaction_id} {TAX} {chat_id}"),
                InlineKeyboardButton("رفض", callback_data=f"reject {transaction_id} {TAX} {chat_id}"),
            ]
                ]

        return keyboard
def parse_mode():
      return 'HTML'   

def chat__id(chat_id):
      return chat_id
def reply_markup(transaction_id , TAX , chat_id):
     keyboard = getKeyboard(transaction_id ,TAX ,chat_id)
     reply_markup = InlineKeyboardMarkup(keyboard)
     return reply_markup

def reply_text(text:str):

    #   text =  f"""🆕 :طلب سحب جديد
    #     🆔 رقم الطلب: #{transfeer_id}
    #     📌 طريقة التحويل: {provider_type}
    #     📌 الرقم: {withdraw_number}
    #     👤 العضو: <a href="tg://user?id={telegram_id}">{telegram_username}</a>
    #     💰المبلغ: {value}
    #     💰النسبة المئوية للاقتطاع: {TAX*100}%
    #     💰المبلغ المقتطع: {value*TAX}
    #     💰 المبلغ المستحق بعد الاقتطاع: {value - value*TAX} SYP
    #     📅 تاريخ الإنشاء: {transfeer_date}"""
    
      text =text.replace("تم استلام طلبك وسيتم إعلامك عند معالجته\n" , "")
      return text