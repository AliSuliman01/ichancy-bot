import Logger
from messages.approveDepositFromAdmin import deposit_message
from models.transaction import Transaction
logger = Logger.getLogger()

async def handler(query ,context ):
    text = deposit_message()
    await query.edit_message_text(
        text = query.message.text + "\n\n"+"تم تأكيد الطلب",
    )
    print(query)
    user_id =  query.message.entities[0].user.id
    await context.bot.send_message(chat_id=user_id, text=text)  