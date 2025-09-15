import executing.executingInterface as interface
import flows.guideHandlers.howWithdrawTelegramAccount.handler
class HowWithdrawTelegramAccountExecute(interface):
    async def execute(self  ,query ,  **kwargs):
        await flows.guideHandlers.howWithdrawTelegramAccount.handler.handler(query)

    