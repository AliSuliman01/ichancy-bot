from telegram import Update
from telegram.ext import ContextTypes ,CallbackContext

PASSWORD = 2
async def get_username(update: Update, context: CallbackContext) -> int:
    username = update.message.text 
    email = username + "@gilbert.com"
    context.user_data['email'] = email
    context.user_data['username'] = username
    print(")))))))))))))))))))))))))))))))))))))))))))))))))))")
    print(context)
    print(")))))))))))))))))))))))))))))))))))))))))))))))))))")
    await update.message.reply_text(text=
        "ادخل كلمة المرور" ,parse_mode='Markdown'
    )
    return PASSWORD