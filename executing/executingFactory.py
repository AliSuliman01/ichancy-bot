import flows.backToMenu.execute
import flows.contactUs.execute
import flows.ichancy.execute
import flows.withdrawal.execute
import flows.deposit.execute
import flows.terms.execute
import flows.problemInBot.execute
import flows.problemInWebsite.execute
import flows.guideHandlers.whatIchancy.execute
import flows.guideHandlers.guides.execute
import flows.guideHandlers.HowDepositIchancyAccount.execute
import flows.guideHandlers.HowDepositTelegramAccount.execute
import flows.guideHandlers.howWithdrawIchancyAccount.execute
import flows.guideHandlers.howWithdrawTelegramAccount.execute
import flows.guideHandlers.HowToCreateNewAccount.execute
import executing.executingInterface
import flows.approveDepositFromAdmin.execute
import flows.rejectDepositFromAdmin.execute
class ExecutingFactury:
    
    def __init__(self):
        self.executes = {
            'back_to_menu' : flows.backToMenu.execute.BackToMenuExecute(),
            'ichancy' : flows.ichancy.execute.IchancyExecute(),
            'withdrawal' : flows.withdrawal.execute.WithdrawalExecute(),
            'deposit' : flows.deposit.execute.DepositExecute(),
            'terms_and_conditions' : flows.terms.execute.TermsExecute(),
            'contact_us' : flows.contactUs.execute.ContactUsExecute(),
            'problem_in_bot' : flows.problemInBot.execute.ProblemInBotExecute(),
            'problem_in_website':flows.problemInWebsite.execute.ProblemInWebsiteExecute(),
            'guides' : flows.guideHandlers.guides.execute.GuidesExecute(),
            'guides_what_is_ichancy' : flows.guideHandlers.whatIchancy.execute.WhatIchancyExecute(),
            'guides_how_deposit_telegram_account' : flows.guideHandlers.HowDepositTelegramAccount.execute.HowDepositTelegramAccountExecute(),
            'guides_how_to_create_new_account' : flows.guideHandlers.HowToCreateNewAccount.execute.HowToCreateNewAccountExecute(),
            'guides_how_withdraw_telegram_account' : flows.guideHandlers.howWithdrawTelegramAccount.execute.HowWithdrawTelegramAccountExecute(),
            'guides_how_deposit_ichancy_account' : flows.guideHandlers.HowDepositIchancyAccount.execute.HowDepositIchancyAccountExecute(),
            'guides_how_withdraw_ichancy_account' : flows.guideHandlers.howWithdrawIchancyAccount.execute.HowWithdrawIchancyAccountExecute(),
            'approve_deposit' : flows.approveDepositFromAdmin.execute.ApproveDepositeFromAdmin(),
            'reject' : flows.rejectDepositFromAdmin.execute.RejectDepositeFromAdmin(),
            'approve_withdraw' : flows.approveDepositFromAdmin.execute.ApproveDepositeFromAdmin(),
        }
        

    async def get_execute(self , execute_name) -> executing.executingInterface.ExecutingInterface: 
        return  self.executes.get(execute_name)
    
