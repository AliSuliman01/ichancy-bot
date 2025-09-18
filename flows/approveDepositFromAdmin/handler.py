from messages.approveDepositFromAdmin import deposit_message
from models.user import User
from models.transaction import Transaction
from models.syriatelTransaction import SyriatelTransaction
from models.model import Model
async def handler(query ,context ):
    text = deposit_message()[0] +'\n'+ query.message.text
    await query.edit_message_text(

        text = text
    )

    transaction_id = query.data.split(" ")[1]
    transaction = Transaction().getById(transaction_id)
    provider_type = transaction.get('provider_type')
    provider_id = int(transaction.get('provider_id'))
    print(query.message.entities[0].user.id)
    user_id =  query.message.entities[0].user.id
    balance = User().getBy({'telegram_id' : ('=' , user_id)})[0].get('balance')

    value = int(transaction.get('value'))
    newBalance = balance + value
    User().update({'telegram_id':('=' , user_id)},{'balance':newBalance})
    t = Transaction().getBy({'provider_id':('=' , provider_id ) ,'provider_type': ('=',provider_type)})
    Transaction().update({'provider_id':('=' , provider_id ) ,'provider_type': ('=',provider_type)},{'status':'approved'})
    transfeer_model = Model
    
    
    match(provider_type):
        case "syriatel" :
            transfeer_model = SyriatelTransaction()
    



    transfeer_model.update({'id':('=' , provider_id)} ,{'status' : 'approved'})
    await context.bot.send_message(chat_id=user_id, text=text)  