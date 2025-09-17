from telegram.ext import CallbackContext , ConversationHandler
from telegram import  Update 
from models.user import User
from models.accountTransaction import AccountTransaction
from iChancyAPI import iChancyAPI
import config.ichancy
from flows.withdrawalAccount.validations import accountBalanceSuficient , isDigit


async def get_withdraw_ammount(update:Update , context: CallbackContext):
    telegram_id = update.message.from_user.id
    user = User().getBy({'telegram_id':('=' , telegram_id)})[0]
    playerId= user.get('player_id')
    balance = user.get('balance')
    user_id = user.get('id')


    api = iChancyAPI()
    accountBalance = api.getPlayerBalanceById(playerId)
    ammountToWithdraw = update.message.text
    if not isDigit.isDigit(ammountToWithdraw):
         await update.message.reply_text("يرجى إدخال رقم صحيح !")
         return ConversationHandler.END
    ammountToWithdraw = int(ammountToWithdraw)
    if not accountBalanceSuficient.validate(accountBalance , ammountToWithdraw):
        await update.message.reply_text("عذرا ليس لديك الرصيد الكافي ")
        return ConversationHandler.END
    
    
    api.WirhdrawMoney(playerId ,ammount=ammountToWithdraw)

    AccountTransaction().insert({'user_id' : user_id , 'status' : "done" , 'action_type':"withdraw" , 'value' : -ammountToWithdraw})
    newBalance = balance + ammountToWithdraw*config.ichancy.EXCHANGE_RATE
    User().update({'telegram_id':('=' , telegram_id)},{'balance' : newBalance})
    await update.message.reply_text('تم استلام المبلغ بنجاح')
    return ConversationHandler.END

