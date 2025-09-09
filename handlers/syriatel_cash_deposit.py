from iChancyAPI import iChancyAPI
import asyncio
import Logger , store
from telegram import Update,ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)

logger = Logger.getLogger()

transfer_num, value = range(2)
# معالجة الضغط على الزر الداخلي
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'syriatel_cash_deposit':
        await query.edit_message_text(
            text=(
                "ارسل الى احد الارقام التالية بطريقة التحويل اليدوي\n"
                "83935571\n"
                "00229271\n\n"
                "اقل قيمة للشحن هي 25,000\n"
                "وأي قيمة أقل من 25,000 لا يمكن شحنها او استرجاعها\n"
                "ثم ادخل رقم عملية التحويل  👇\n"
            )
        )
        return transfer_num

    return ConversationHandler.END

async def get_transfer_num(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    telegram_user_id = str(update.effective_user.id)
    transfer_num = update.message.text
    context.user_data['transfer_num'] = transfer_num
    logger.info("User %s entered transfer number: %s", user.first_name, transfer_num)
    await update.message.reply_text(
        f"ادخل المبلغ الذي ارسلته بالليرة السورية"
    )
    return value

async def get_value(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    value = update.message.text
    context.user_data['value'] = value
    logger.info("User %s set value: %s", user.first_name, value)
    asyncio.create_task(handle_create_transaction(update , context=context))
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        'تم إلغاء عملية الشحن.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def conversationHandler():
    conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern='^syriatel_cash_deposit$')],
    states={
        transfer_num: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transfer_num)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler
async def handle_create_transaction(update: Update ,context: ContextTypes.DEFAULT_TYPE):
    """Handle account creation"""
    try:
        telegram_user_id = str(update.effective_user.id)
        transfer_num=context.user_data.get('transfer_num')
        value=context.user_data.get('value')
        api = iChancyAPI()
        logger.info(api.COOKIES)

        syriatelCashTransaction = store.insertSyriatelCashTransaction(telegram_id = telegram_user_id,transfer_num=transfer_num,value=value)
        
        success_text = (
            "طلب شحن\n"
            "Syriatel Cash 🟢\n"
            "رقم العملية او العنوان: " + str(transfer_num) + "\n\n"
            "المبلغ بالليرة:  " + str(value) + "\n"
            "قيمة الطلب: " + str(value) + "\n"
            "رقم الطلب: #" + str(syriatelCashTransaction['id']) + "\n"
        )
        
        await update.message.reply_text(success_text ,parse_mode='Markdown')

 
    except Exception as e:
        logger.error(f"Error in handle_create_transaction: {e}")
  
    context.user_data.pop('transfer_num', None)
    context.user_data.pop('value', None)