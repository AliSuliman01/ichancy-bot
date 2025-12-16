from telegram.ext import CallbackContext , ConversationHandler
from telegram import  Update 
from models.user import User
from models.accountTransaction import AccountTransaction
from iChancyAPI import iChancyAPI
import config.ichancy ,config.telegram
from flows.withdrawalAccount.validations import accountBalanceSuficient , isDigit
import asyncio
from threading import Thread
from database import Database
async def get_withdraw_ammount(update:Update , context: CallbackContext):
         await update.message.reply_text("المعالجة جارية")
         task = asyncio.create_task(handling(update , context))
         if 'background_tasks' not in context.application.bot_data:
              context.application.bot_data['background_tasks'] = set()
         context.application.bot_data['background_tasks'].add(task)
         task.add_done_callback(lambda t: context.application.bot_data['background_tasks'].discard(t))
         return ConversationHandler.END
    
async def handling(update , context):
   db = Database.getConnection()
   try:
    if db:
        db.start_transaction()
        cursor = db.cursor(dictionary=True)
        telegram_id = update.message.from_user.id
        user = User(cursor).getBy({'telegram_id':('=' , telegram_id)})[0]
        playerId= user.get('player_id')
        balance = user.get('balance')
        user_id = user.get('id')
        ammountToWithdraw = update.message.text
        counter = 0
        while True:
            counter+=1
            if(config.telegram.COOKIE_STATUS):
                api = iChancyAPI()
                accountBalance = await api.getPlayerBalanceById(playerId)
                if accountBalance.get('success'):
                    await asyncio.sleep(0.2)
                    break
            if counter > 40:
                await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                await update.message.reply_text("البوت بحالة صيانة دورية وسيعود للعمل قريبا")
                return
            await asyncio.sleep(5)

        if accountBalance.get('success'):
            
            accountBalance = accountBalance.get('data')
            if not isDigit.isDigit(ammountToWithdraw):
                await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                await update.message.reply_text("يرجى إدخال رقم صحيح !")
                return
            ammountToWithdraw = int(ammountToWithdraw)
            await  api.WirhdrawMoney(playerId ,ammount=ammountToWithdraw)
            if not accountBalanceSuficient.validate(accountBalance , ammountToWithdraw):
                await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                await update.message.reply_text("عذرا ليس لديك الرصيد الكافي ")
                return
        else:
            await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
            await update.message.reply_text("البوت بحالة صيانة دورية وسيعود للعمل قريبا")
            return
    
        AccountTransaction(cursor).insert({'user_id' : user_id , 'status' : "done" , 'action_type':"withdraw" , 'value' : -ammountToWithdraw})
        newBalance = balance + ammountToWithdraw*config.ichancy.EXCHANGE_RATE
        User(cursor).update({'telegram_id':('=' , telegram_id)},{'balance' : newBalance})
        await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
        await update.message.reply_text('تم استلام المبلغ بنجاح')
        db.commit()
        return
   except Exception as e:
       db.rollback()
    
   finally:
       if db:
           db.close()