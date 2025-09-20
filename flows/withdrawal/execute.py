import executing.executingInterface as interface
import flows.withdrawal.handler
class WithdrawalExecute(interface.ExecutingInterface):

    async def execute(self , query , **kwargs):
        await flows.withdrawal.handler.handler(query)

    