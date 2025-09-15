import executing.executingInterface as interface
import flows.guideHandlers.HowDepositIchancyAccount.handler
class HowDepositIchancyAccountExecute(interface.ExecutingInterface):

    async def execute(self  ,query ,  **kwargs):
        await flows.guideHandlers.HowDepositIchancyAccount.handler.handler(query)

    