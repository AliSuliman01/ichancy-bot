import executing.executingInterface as interface
import flows.guideHandlers.howWithdrawIchancyAccount.handler
class HowWithdrawIchancyAccountExecute(interface.ExecutingInterface):
    async def execute(self  ,query ,  **kwargs):
        await flows.guideHandlers.howWithdrawIchancyAccount.handler.handler(query)

    