from messages.rejectDepositFromAdmin import deposit_message
from models.user import User
from models.transaction import Transaction
from models.syriatelTransaction import SyriatelTransaction
from database import Database
async def handler(query ,context ):
   db = Database.getConnection()
   try:
    if db:
        db.start_transaction()
        cursor = db.cursor(dictionary = True)
        text = deposit_message()[0] +'\n'+ query.message.text
        await query.edit_message_text(text)

        transaction_id = query.data.split(" ")[1]
        transaction = Transaction(cursor).getById(transaction_id)
        provider_type = transaction.get('provider_type')
        provider_id = int(transaction.get('provider_id'))
        user_id =  query.message.entities[len(query.message.entities)-1].user.id

        Transaction(cursor).update({'provider_id':('=' , provider_id ) ,'provider_type': ('=',provider_type)},{'status':'rejected'})
        if provider_type.find('Syriatel') != -1 :
            SyriatelTransaction(cursor).update({'id':('=' , provider_id)} ,{'status' : 'rejected'})
        await context.bot.send_message(chat_id=user_id, text=text)  
        db.commit()
   except Exception as e:
      db.rollback()
    
   finally:
        if db:
           db.close()
