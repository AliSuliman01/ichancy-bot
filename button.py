from telegram import Update
from telegram.ext import ContextTypes
from models.user import User
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button presses"""
    query = update.callback_query
    await query.answer() 
    user_id = str(update.effective_user.id)
    username = update.effective_user.username
    data = "."
    data = update.callback_query.data.split(" ")[0]
    ##################################################################
    import executing.executingFactory
    execute = executing.executingFactory.ExecutingFactury()
    
    button = await execute.get_execute(data)
    # context.bot.edit_message_text()
    if button:
        await button.execute(query=query, username=username , user_id=user_id , context = context)

