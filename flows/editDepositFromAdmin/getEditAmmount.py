from telegram import  Update
from telegram.ext import CallbackContext , ConversationHandler
from models.transaction import Transaction
from models.model import Model
from models.syriatelTransaction import SyriatelTransaction
from config.telegram import ADMIN_ID
from models.user import User
from models.bemoTransaction import BemoTransaction
from models.shamCashTransaction import ShamCashTransaction
from models.cryptoTransaction  import CryptoTransaction
from models.orderMoney import OrderMoneyTransaction
import config.crypto
import time
from flows.editDepositFromAdmin.validation import validationEditAmmount ,messageWasNotEditedYet
from database import Database



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
        currency = context.user_data["currency"]
        realValue = context.user_data["realValue"]
        transaction_id = int(context.user_data["transaction_id"])
        chat_id = context.user_data["chat_id"]
        transaction = Transaction(cursor).getById(transaction_id)
        provider_type , provider_id = getDataFromTransaction(transaction)
    
    
        message = context.user_data["message"]
        user = User(cursor).getById(transaction.get('user_id'))
        edited_message = getEditedMessage(message , transaction ,user , edit_ammount ,realValue)

        provider_model = getProviderModel(provider_type , cursor)
        updateTransactionsTables(provider_model , provider_id ,edit_ammount ,transaction_id , cursor ,currency)
        
        
        await context.bot.edit_message_text(message_id=context.user_data["message_id"],chat_id=chat_id ,text = edited_message, reply_markup = context.user_data["reply_markup"],parse_mode = 'HTML')
        await removeMessages(update , context , chat_id)
        db.commit()
        return ConversationHandler.END
   except Exception as e:
       print (e)
       db.rollback()
   finally:
       if db:
           db.close()



async def removeMessages(update , context , chat_id):
    
    time.sleep(0.5)
    await context.bot.delete_message(message_id = update.message.id , chat_id = chat_id)
    await context.bot.delete_message(message_id = update.message.id-1 , chat_id = chat_id)



def getEditedMessage(message ,transaction , user , edit_ammount , realValue):
    
    edited_message = message.replace("المبلغ: " + str(realValue),"المبلغ: " + str(edit_ammount))
    edited_message = edited_message.replace(user.get('telegram_username') , f"""<a href="tg://user?id={user.get('telegram_id')}">{user.get('telegram_username')}</a>""")
    
    if messageWasNotEditedYet.validate(edited_message):
        edited_message = "تم تعديل القيمة من قبل الأدمن !!\n\n" + edited_message
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
            case "crypto":
                provider_model = CryptoTransaction(cursor)
    
    return provider_model


def getDataFromTransaction(transaction:dict):
    provider_type = transaction.get('provider_type')
    provider_id = int(transaction.get('provider_id'))
    return provider_type , provider_id 


def updateTransactionsTables(provider_model , provider_id  , edit_ammount , transaction_id ,cursor ,currency):
    edit_ammount = float(edit_ammount)*float(config.crypto.SYP_for_unit[currency])
    Transaction(cursor).update({'id': ('=',transaction_id)},{'value':edit_ammount})
    provider_model.update({'id':('=' ,provider_id)} , {'value':edit_ammount})