from telegram import  Update
from telegram.ext import CallbackContext , ConversationHandler
from models.transaction import Transaction
from models.model import Model
from models.syriatelTransaction import SyriatelTransaction
from config.telegram import ADMIN_ID
from models.user import User
import time
from flows.editDepositFromAdmin.validationEditAmmount import validate
async def get_edit_ammount(update: Update, context: CallbackContext) -> int:
    edit_ammount = update.message.text
    if not validate(edit_ammount):
        await update.message.reply_text(text="يرجى إدخال قيمة صحيحية")
        return ConversationHandler.END
    transaction_id = int(context.user_data["transaction_id"])
    print(transaction_id)
    transaction = Transaction().getById(transaction_id)
    Transaction().update({'id': ('=',transaction_id)},{'value':edit_ammount})
    provider_type = transaction.get('provider_type')
    provider_id = transaction.get('provider_id')
    print(transaction)
    transfeer_model = Model
    match provider_type :
        case "syriatel":
            transfeer_model = SyriatelTransaction()

    transfeer_model.update({'id':('=' ,provider_id)} , {'value':edit_ammount})
    user = User().getById(transaction.get('user_id'))
    message:str
    message = context.user_data["message"]
    edited_message = message.replace("المبلغ: " + str(transaction.get('value')),"المبلغ: " + str(edit_ammount))
    edited_message = edited_message.replace(user.get('telegram_username') , f"""<a href="tg://user?id={user.get('telegram_id')}">{user.get('telegram_username')}</a>""")
    if edited_message.find("تعديل") ==-1:
        edited_message = "تم تعديل القيمة من قبل الأدمن !!\n\n" + edited_message
    await context.bot.edit_message_text(message_id=context.user_data["message_id"],chat_id=ADMIN_ID ,text = edited_message, reply_markup = context.user_data["reply_markup"],parse_mode = 'HTML')
    time.sleep(0.5)
    await context.bot.delete_message(message_id = update.message.id , chat_id = ADMIN_ID)
    await context.bot.delete_message(message_id = update.message.id-1 , chat_id = ADMIN_ID)
    return ConversationHandler.END