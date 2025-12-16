import executing.executingInterface as interface
import flows.guideHandlers.HowDepositTelegramAccount.handler
class HowDepositTelegramAccountExecute(interface.ExecutingInterface):

    async def execute(self  ,query ,  **kwargs):
        await flows.guideHandlers.HowDepositTelegramAccount.handler.handler(query)

    