from logging import config
from messages.approveDepositAndWithdrawalFromAdmin import message
from models.user import User
from models.transaction import Transaction
from models.syriatelTransaction import SyriatelTransaction
from models.bemoTransaction import BemoTransaction
from models.shamCashTransaction import ShamCashTransaction
from models.cryptoTransaction import CryptoTransaction
import config.crypto
from database import Database
async def handler(query ,context ):
   db = Database.getConnection()
   try:
    if db:
        db.start_transaction()
        cursor = db.cursor(dictionary=True)
        text = message()[0] +'\n'+ query.message.text
        await query.edit_message_text(text)
        transaction_id = query.data.split(" ")[1]
        transaction = Transaction(cursor).getById(transaction_id)
        provider_type, provider_id , value=  getDataFromTransaction(transaction)
        user_id =  query.message.entities[0].user.id
        updateUserBalance(user_id , value , cursor)
        provider_model = getProviderModel(provider_type , cursor)
        updateTransactionsTables(provider_model ,provider_id ,provider_type , cursor)
        
        await context.bot.send_message(chat_id=user_id, text=text)  
        db.commit()
   except Exception as e:
       print (e)
       db.rollback()
   finally:
       if db:
           db.close()


def getDataFromTransaction(transaction:dict):
    provider_type = transaction.get('provider_type')
    provider_id = int(transaction.get('provider_id'))
    value = int(transaction.get('value'))
    return provider_type , provider_id ,value

def updateUserBalance(user_id ,value , cursor):
    balance = User(cursor).getBy({'telegram_id' : ('=' , user_id)})[0].get('balance')
    newBalance = balance + value
    print("####################################################")
    print(newBalance)
    User(cursor).update({'telegram_id':('=' , user_id)},{'balance':newBalance})



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


def updateTransactionsTables(provider_model , provider_id , provider_type , cursor):
    Transaction(cursor).update({'provider_id':('=' , provider_id ) ,'provider_type': ('=',provider_type)},{'status':'approved'})
    provider_model.update({'id':('=' , provider_id)} ,{'status' : 'approved'})