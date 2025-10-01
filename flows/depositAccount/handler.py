import asyncio
from telegram.ext import ConversationHandler , MessageHandler ,filters ,CallbackQueryHandler ,CommandHandler
from telegram import Update
from flows.depositAccount.cancel import cancel
from flows.depositAccount.entryPoint import button_deposit_account_handler
from flows.depositAccount.ammountState import get_ammount_for_deposit
from models.user import User
from iChancyAPI import iChancyAPI
from flows.depositAccount.validations import balanceSuficient , adminBalanceSuficient , isDigit
import config.ichancy
from models.accountTransaction import AccountTransaction
from database import Database
AMMOUNT = 1
def conversationHandler():
   
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_deposit_account_handler , pattern = "^deposit_account$")],
        states={
            AMMOUNT :[MessageHandler(filters.TEXT & ~filters.COMMAND , get_ammount_for_deposit)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    return conv_handler


async def finishungHandling(update:Update , context):
   db = Database.getConnection()
   try:
    db.start_transaction()
    cursor = db.cursor(dictionary = True)
    telegram_id = update.message.from_user.id
    user = User(cursor).getBy({'telegram_id' : ('=' , telegram_id)})[0]
    playerId= user.get('player_id')
    balance = user.get('balance')
    user_id = user.get('id')
    ammountForDeposit = update.message.text


    if isDigit.isDigit(ammountForDeposit):
        ammountForDeposit = int(ammountForDeposit)
        if balanceSuficient.validate(balance , ammountForDeposit):
            counter = 0
            while True:
                counter+=1
                api = iChancyAPI()
                adminBalanceInfo = await api.getAdminstratorBalance()
                if adminBalanceInfo['success']:
                    adminBalance = adminBalanceInfo['data']
                    if adminBalanceSuficient.validate(adminBalance , ammountForDeposit):
                        newBlanceForPlaryer = balance - ammountForDeposit*config.ichancy.EXCHANGE_RATE 
                        User(cursor).update({'telegram_id': ('=',telegram_id)} , {'balance': newBlanceForPlaryer})     
                        AccountTransaction(cursor).insert({
                        'user_id': user_id,
                        'status' : 'done',
                        'action_type': 'deposit',
                        'value':ammountForDeposit
                        })
                        await api.transfeerMoney(ammount=ammountForDeposit, player_id=playerId)
                        await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                        await update.message.reply_text("تمت العملية بنجاح")
                        db.commit()
                        db.close()
                        return 
                    else:
                        await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                        await update.message.reply_text("فشلت العملية!")
                        db.close()
                        return 
                if counter > 40:
                    await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
                    await update.message.reply_text("خطأ بالموقع وسيعود للعمل قريبا")
                    db.close()
                    return
                await asyncio.sleep(5)
        else:
            await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
            await update.message.reply_text("فشلت العملية ليس معك رصيد كافٍ!")
            db.close()
            return 
    else:
        await context.bot.delete_message(message_id = update.message.id+1 , chat_id = update.message.from_user.id)
        await update.message.reply_text("يرجى إدخال رقم صحيح!")
        db.close()
        return 
   except Exception as e:
       print (e)
       db.rollback()