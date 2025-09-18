from messages.approveDepositFromAdmin import deposit_message
from models.user import User
from models.transaction import Transaction
from models.syriatelTransaction import SyriatelTransaction
from models.bemoTransaction import BemoTransaction
async def handler(query ,context ):
    text = deposit_message()[0] +'\n'+ query.message.text
    await query.edit_message_text(text)

    transaction_id = query.data.split(" ")[1]
    transaction = Transaction().getById(transaction_id)

    provider_type, provider_id , value=  getDataFromTransaction(transaction)
    user_id =  query.message.entities[0].user.id

    updateUserBalance(user_id , value)
    provider_model = getProviderModel(provider_type)
    updateTransactionsTables(provider_model ,provider_id ,provider_type)
    
    await context.bot.send_message(chat_id=user_id, text=text)  



def getDataFromTransaction(transaction:dict):
    provider_type = transaction.get('provider_type')
    provider_id = int(transaction.get('provider_id'))
    value = int(transaction.get('value'))
    return provider_type , provider_id ,value

def updateUserBalance(user_id ,value):
    balance = User().getBy({'telegram_id' : ('=' , user_id)})[0].get('balance')
    newBalance = balance + value
    User().update({'telegram_id':('=' , user_id)},{'balance':newBalance})



def getProviderModel(provider_type):
    provider_model = None
    match(provider_type):
            case "syriatel" :
                provider_model = SyriatelTransaction()
            case "bemo" :
                provider_model = BemoTransaction()

    return provider_model


def updateTransactionsTables(provider_model , provider_id , provider_type):
    Transaction().update({'provider_id':('=' , provider_id ) ,'provider_type': ('=',provider_type)},{'status':'approved'})
    provider_model.update({'id':('=' , provider_id)} ,{'status' : 'approved'})