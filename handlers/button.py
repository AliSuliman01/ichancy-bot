from telegram import Update
from telegram.ext import ContextTypes
from models.user import User
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button presses"""
    query = update.callback_query
    await query.answer() 
    user_id = str(update.effective_user.id)
    username = update.effective_user.username
    data = query.data
    ##################################################################
    import executing.executingFactory
    execute = executing.executingFactory.ExecutingFactury()

    button = await execute.get_execute(data)

    if button:
        await button.execute(query=query, username=username , user_id=user_id)


    ##################################################################
#     if data.find('guide') != -1:
#         await guidesButton(update , context , query)
#     # elif data == 'check_status':
#     #     await handlers.checkStatus.handle_check_status(query, user_id)
#     # elif data == 'help':
#     #     await handlers.help.handle_help(query)
#     elif data == 'back_to_menu':
#         await flows.backToMenu.handler.handler(query , username)
#     elif data == 'ichancy':
#         await flows.ichancy.handler.handler(query, user_id)
#     elif data == 'withdrawal':
#         await flows.withdrawal.handler.handler(query , user_id)
#     elif data == 'deposit':
#         await flows.deposit.handler.handler(query , user_id)
#     elif data == 'terms_and_conditions':
#         await flows.terms.handler.handler(query)
#     elif data == 'contact_us':
#         await flows.contactUs.handler.handler(query)
#     elif data =='problem_in_bot':
#          await flows.problemInBot.handler.handler(query)
#     elif data =='problem_in_website':
#          await handlers.problemInWebsite.handle_problem_in_website(query)
    # if data == 'confirm_syriatel_cash_deposit':
    #     await handlers.syriatel_cash_deposit.confirm_deposit(update, context)
    # elif data.startswith('approve_'):
    #     _, transaction_type, transaction_id = data.split('_')
    #     await handlers.transactions.approve_transaction(query, transaction_id,transaction_type)
    # elif data.startswith('reject_'):
    #     _, transaction_type, transaction_id = data.split('_')
    #     await handlers.transactions.reject_transaction(query, transaction_id, transaction_type)

# async def guidesButton(update: Update, context: ContextTypes.DEFAULT_TYPE , query):
#     data = query.data
#     if data == "guides":
#         await flows.guideHandlers.guides.handler.handler(query)
#     elif data == "guides_what_is_ichancy":
#         await flows.guideHandlers.whatIchancy.handler.handler(query)
#     elif data == "guides_how_deposit_telegram_account":
#         await flows.guideHandlers.HowDepositTelegramAccount.handler.handler(query)
#     elif data == "guides_how_to_create_new_account":
#         await flows.guideHandlers.HowToCreateNewAccount.handler.handler(query)
#     elif data == "guides_how_withdraw_telegram_account":
#         await flows.guideHandlers.howWithdrawTelegramAccount.handler.handler(query)
#     elif data == "guides_how_deposit_ichancy_account":
#         await flows.guideHandlers.HowDepositIchancyAccount.handler.handler(query)
#     elif data == "guides_how_withdraw_ichancy_account":
#         await flows.guideHandlers.howWithdrawIchancyAccount.handler.handler(query)