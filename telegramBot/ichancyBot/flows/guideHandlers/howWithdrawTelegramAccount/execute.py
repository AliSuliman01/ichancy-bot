import executing.executingInterface as interface
import flows.guideHandlers.howWithdrawTelegramAccount.handler
class HowWithdrawTelegramAccountExecute(interface.ExecutingInterface):
    async def execute(self  ,query ,  **kwargs):
        await flows.guideHandlers.howWithdrawTelegramAccount.handler.handler(query)

    