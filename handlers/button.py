import handlers.checkStatus , handlers.ichancy , handlers.backToMenu, handlers.help, handlers.withdrawal, handlers.deposit
from telegram import Update
from telegram.ext import ContextTypes
import handlers.command.start
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button presses"""
    query = update.callback_query
    await query.answer() 
    user_id = str(update.effective_user.id)
    username = update.effective_user.username
    data = query.data
    
    
    if data == 'check_status':
        await handlers.checkStatus.handle_check_status(query, user_id)
    elif data == 'help':
        await handlers.help.handle_help(query)
    elif data == 'back_to_menu':
        await handlers.backToMenu.handle_back_to_menu(query ,username)
    elif data == 'ichancy':
        await handlers.ichancy.handle_ichancy(query , user_id)
    elif data == 'withdrawal':
        await handlers.withdrawal.handle_withdrawal(query , user_id)
    elif data == 'deposit':
        await handlers.deposit.handle_deposit(query , user_id)