import Logger
from telegram import  InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler,CallbackContext
from models.syriatelTransaction import SyriatelTransaction
from models.user import User
import config.telegram
logger = Logger.getLogger()

async def get_value(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    value = update.message.text
    if str.isdigit(value):
        transfer_num = context.user_data['transfer_num']
        telegram_id = update.message.from_user.id
        user = User().getBy({'telegram_id':('=', telegram_id)})[0]
        user_id = user.get('id')
        SyriatelTransaction().insert({'transfer_num' : transfer_num , 'user_id': user_id , 'status':'pending','action_type':'deposit' , 'value' : value})
        transfeer_id = SyriatelTransaction().getBy({'transfer_num' : ('=', transfer_num)})[0].get('id')
        message = (
            "تم استلام طلبك وسيتم إعلامك عند معالجته\n\n"
            "طلب شحن :\n"
            "Syriatel Cash 🟢\n"
            "كود العملية :\n" + transfer_num + "\n"
            "المبلغ بالليرة : " + value + "\n"
            "رقم الطلب : #" + str(transfeer_id)  + "\n"
        )
        await update.message.reply_text(message)
        await  send_transaction_to_admin()
    else:
         await update.message.reply_text(
            "يرجى إدخال قيمة صحيحة")

    # await handle_create_transaction(update , context=context)
    return ConversationHandler.END


async def send_transaction_to_admin(transaction_data, transaction_type):
    """Send transaction notification to admin for approval"""
    try:
        from telegram import Bot
        from config.telegram import TOKEN, ADMIN_TELEGRAM_ID, ADMIN_CHAT_ID
        import trans
        from models.user import User
        
        bot = Bot(token=TOKEN)
        
        user = User().getBy({'telegram_id':('=' , transaction_data['user_id'])})
        user_info = f"@{user[2]}" if user and user[2] else "No username"
        #context.bot.get_chat('telegram_id)
        # Get Arabic translation for action type
        action_type_ar = trans.trans['ar'].get(transaction_data['action_type'], transaction_data['action_type'])
        
        message = f"""
🆕 طلب {action_type_ar} جديد

🆔 رقم الطلب: #{transaction_data['id']}
📌 طريقة التحويل: {transaction_type}
👤 العضو: {user_info}
💰 المبلغ: {transaction_data['value']} SYP
📅 تاريخ الإنشاء: {transaction_data['created_at']}
        """
        
        if 'transfer_num' in transaction_data and transaction_data['transfer_num']:
            message += f"\n🔢 رقم عملية التحويل: {transaction_data['transfer_num']}"
        
        keyboard = [
            [
                InlineKeyboardButton("✅ تأكيد", callback_data=f'approve_{transaction_type}_{transaction_data["id"]}'),
                InlineKeyboardButton("❌ رفض", callback_data=f'reject_{transaction_type}_{transaction_data["id"]}')
            ],
            # [InlineKeyboardButton("👁️ View Details", callback_data=f'view_{transaction_data["id"]}')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Prefer ADMIN_CHAT_ID (e.g., a group) if provided to avoid 403 when admin hasn't started the bot
        target_chat_id = ADMIN_CHAT_ID if ADMIN_CHAT_ID else ADMIN_TELEGRAM_ID
        try:
            await bot.send_message(chat_id=target_chat_id, text=message, reply_markup=reply_markup)
        except Exception as e:
            # Common case: Forbidden: bot can't initiate conversation with a user
            err_text = str(e)
            if 'Forbidden' in err_text and 'initiate conversation' in err_text and not ADMIN_CHAT_ID:
                logger.error("Transactions bot can't message ADMIN_TELEGRAM_ID. Ask the admin to open the transactions bot and press /start, or set ADMIN_CHAT_ID to a group the bot is in.")
            raise
        
    except Exception as e:
        logger.error(f"Error sending transaction to admin: {e}")
