from telegram import  Update
from telegram.ext import CallbackContext , ConversationHandler
from models.transaction import Transaction
from models.syriatelTransaction import SyriatelTransaction
from config.telegram import ADMIN_ID
from models.user import User
from models.bemoTransaction import BemoTransaction
from models.shamCashTransaction import ShamCashTransaction
from models.orderMoney import OrderMoneyTransaction
import time
from flows.editWithdrawFromAdmin.validation import validationEditAmmount ,messageWasNotEditedYet
from database import Database
import Logger

logger = Logger.getLogger()



async def get_edit_ammount(update: Update, context: CallbackContext) -> int:
   db = Database.getConnection()
   try:
    if db:
        db.start_transaction()
        cursor = db.cursor(dictionary = True)
        edit_ammount = update.message.text
        if not validationEditAmmount.validate(edit_ammount):
            await update.message.reply_text(text="يرجى إدخال قيمة صحيحية")
            return ConversationHandler.END
        
        transaction_id = int(context.user_data["transaction_id"])
        transaction = Transaction(cursor).getById(transaction_id)
        provider_type , provider_id = getDataFromTransaction(transaction)
        chat_id = context.user_data["chat_id"]
        
        message = context.user_data["message"]
        TAX = float(context.user_data["TAX"])
        user = User(cursor).getById(transaction.get('user_id'))
        edited_message = getEditedMessage(message , transaction ,user , edit_ammount ,TAX)

        provider_model = getProviderModel(provider_type , cursor)
        updateTransactionsTables(provider_model , provider_id ,edit_ammount ,transaction_id , cursor)
        
        
        await context.bot.edit_message_text(message_id=context.user_data["message_id"],chat_id=chat_id ,text = edited_message, reply_markup = context.user_data["reply_markup"],parse_mode = 'HTML')
        await removeMessages(update , context , chat_id)
        db.commit()
        return ConversationHandler.END
   except Exception as e:
       # print (e)
       logger.error(f"Error in getEditAmmount: {e}")
       db.rollback()

   finally:
       db.close()



async def removeMessages(update , context ,chat_id):
    
    time.sleep(0.5)
    await context.bot.delete_message(message_id = update.message.id , chat_id = chat_id)
    await context.bot.delete_message(message_id = update.message.id-1 , chat_id = chat_id)



def getEditedMessage(message ,transaction , user , edit_ammount , TAX):
    edited_message = message.replace("المبلغ: " + str(-transaction.get('value')),"المبلغ: " + str(edit_ammount))
    # print(edited_message)
    # print(-transaction.get('value'))
    # print("#"*10)
    edited_message = edited_message.replace("المبلغ المقتطع: " + str(TAX*float(-transaction.get('value'))), "المبلغ المقتطع: "+ str(float(edit_ammount)*TAX))
    edited_message = edited_message.replace("المبلغ المستحق بعد الاقتطاع: "+ str(-transaction.get('value')-float(-transaction.get('value'))*TAX), "المبلغ المستحق بعد الاقتطاع: "+ str(float(edit_ammount)- float(edit_ammount)*TAX))
    edited_message = edited_message.replace(user.get('telegram_username') , f"""<a href="tg://user?id={user.get('telegram_id')}">{user.get('telegram_username')}</a>""")
    # print(edited_message)
    if messageWasNotEditedYet.validate(edited_message):
        edited_message = "تم تعديل القيمة من قبل الأدمن !!\n\n" + edited_message
    # print(edited_message)
    # print(edit_ammount)
    return edited_message


def getProviderModel(provider_type , cursor):
    provider_model = None
    match(provider_type):
            case "syriatel" :
                provider_model = SyriatelTransaction(cursor)
            case "bemo" :
                provider_model = BemoTransaction(cursor)
            case "sham cash":
                provider_model = ShamCashTransaction(cursor)
            case "order money":
                provider_model = OrderMoneyTransaction(cursor)


    return provider_model


def getDataFromTransaction(transaction:dict):
    provider_type = transaction.get('provider_type')
    provider_id = int(transaction.get('provider_id'))
    return provider_type , provider_id 


def updateTransactionsTables(provider_model , provider_id  , edit_ammount , transaction_id , cursor):
    Transaction(cursor).update({'id': ('=',transaction_id)},{'value':-int(edit_ammount)})
    provider_model.update({'id':('=' ,provider_id)} , {'value':-int(edit_ammount)})