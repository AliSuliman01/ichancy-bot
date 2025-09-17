from telegram import Update 
from telegram.ext import CallbackContext
import Logger
import Logger 
from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
logger = Logger.getLogger()

telegramIdGoal = 1
# معالجة الضغط على الزر الداخلي
async def button_send_gifts_handler(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    text = (
    "**ان عملية الاهداء هذه ستكون العملية رقم 1 لليوم وسيتم اقتطاع عمولة بنسبة 0.0% من قيمة المبلغ المرسل** \n\n "
    "ارسل معرف التلغرام للشخص المراد اهداء الرصيد اليه \n"
    " يمكن الحصول على المعرف عن طريق ضغط زر رصيدي\n"
    f"معرف الاهداء الخاص بك هو {telegram_id}\n"
    "ارسل معرف تلغرام المستخدم الذي تريد اهداؤه\n"
    )
    query = update.callback_query
    await query.answer()
    if query.data == 'send_gift':
        await query.edit_message_text(
            text=text ,
            parse_mode='Markdown'
        )
        return telegramIdGoal

    return ConversationHandler.END


