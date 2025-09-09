import Logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes
logger = Logger.getLogger()
def getTextWelcome(username):
    welcome_text = (
            f"أهلا {username} \n "
             "نرحب بك في بوت في بوت Gilbert Ichancy "
        )
    return welcome_text

def getKeyboard():
    keyboard = [
        [InlineKeyboardButton("🆕 Ichancy", callback_data='ichancy')],
        [
            InlineKeyboardButton("شحن رصيد 📥", callback_data='deposit'),
            InlineKeyboardButton("سحب رصيد 📤", callback_data='withdrawal'),
        ],
        [InlineKeyboardButton("📊 Check Account Status", callback_data='check_status')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    return keyboard

def getReplyMarkup():
    reply_markup = InlineKeyboardMarkup(getKeyboard())
    return reply_markup

async def getInfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or update.effective_user.first_name
    logger.info(f"User {username} ({user_id}) started the bot")
    return user_id , username