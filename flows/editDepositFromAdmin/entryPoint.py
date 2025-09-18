from telegram import  Update
from telegram.ext import (

    ConversationHandler,
    CallbackContext,
    )
from config.telegram import ADMIN_ID
EDIT = 1
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    
    await query.answer()
    if query.data.split(" ")[0] == 'edit':
        await context.bot.send_message(chat_id = ADMIN_ID ,
            text="يرجى إدخال القيمة الجديدة بالليرة السورية "
        )
        context.user_data["transaction_id"] = query.data.split(" ")[1]
        context.user_data["message"] = update.callback_query.message.text
        context.user_data["message_id"] = update.callback_query.message.message_id
        context.user_data["reply_markup"] = update.callback_query.message.reply_markup
        return EDIT

    return ConversationHandler.END

#  Update Update(callback_query=CallbackQuery(chat_instance='6850367376347390038', data='edit 60',
#  from_user=User(first_name='Abdullatif', id=1419197314, is_bot=False, language_code='en', last_name='Aleddah'),
#    id='6095406050595634961', message=Message(channel_chat_created=False, 
# chat=Chat(first_name='Abdullatif', id=1419197314, last_name='Aleddah', type=<ChatType.PRIVATE>),
# date=datetime.datetime(2025, 9, 18, 10, 17, 45, tzinfo=<UTC>), delete_chat_photo=False,
# entities=(MessageEntity(length=10, offset=97, type=<MessageEntityType.TEXT_MENTION>,
#            user=User(first_name='Abdullatif', id=1419197314, is_bot=False, language_code='en', last_name='Aleddah')),),
#              from_user=User(first_name='DR.Tooth', id=6618357846, is_bot=True, username='ClashJustForMeBot'),
#            group_chat_created=False, message_id=14533, 
#     reply_markup=InlineKeyboardMarkup(inline_keyboard=((InlineKeyboardButton(callback_data='edit 60', text='تعديل القيمة'),),
#  (InlineKeyboardButton(callback_data='approve 60', text='تأكيد'), InlineKeyboardButton(callback_data='reject 60', text='رفض')))), 
#  supergroup_chat_created=False, text='🆕 :طلب شحن جديد\n        🆔 رقم الطلب: #103\n        📌 طريقة التحويل: syriatel\n        👤 
# العضو: Abdullatif\n        💰 المبلغ: 2020 SYP\n        📅 تاريخ الإنشاء: 2025-09-18 13:17:43')), update_id=299627338)