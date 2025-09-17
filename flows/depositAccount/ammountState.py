from telegram import Update  
from iChancyAPI import iChancyAPI
from telegram.ext import ConversationHandler , ContextTypes
import config.ichancy
from models.user import User
from models.accountTransaction import AccountTransaction
from flows.depositAccount.validations import balanceSuficient , adminBalanceSuficient
async def get_ammount_for_deposit(update: Update , context : ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    user = User().getBy({'telegram_id' : ('=' , telegram_id)})[0]
    playerId= user.get('player_id')
    balance = user.get('balance')
    user_id = user.get('id')
    ammountForDeposit = int(update.message.text)
    if balanceSuficient.validate(balance , ammountForDeposit):
        api = iChancyAPI()
        adminBalance = api.getAdminstratorBalance()
        if adminBalanceSuficient.validate(adminBalance , ammountForDeposit):
            newBlanceForPlaryer = balance - ammountForDeposit*config.ichancy.EXCHANGE_RATE 
            User().update({'telegram_id': ('=',telegram_id)} , {'balance': newBlanceForPlaryer})     
            AccountTransaction().insert({
            'user_id': user_id,
            'status' : 'done',
            'action_type': 'deposit',
            'value':ammountForDeposit
            })
            api.transfeerMoney(ammount=ammountForDeposit, player_id=playerId)
            await update.message.reply_text("تمت العملية بنجاح")
            return ConversationHandler.END
        else:
            await update.message.reply_text("فشلت العملية!")
            return ConversationHandler.END
    else:
        await update.message.reply_text("فشلت العملية ليس معك رصيد كافٍ!")
        return ConversationHandler.END


