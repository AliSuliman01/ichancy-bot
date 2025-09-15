import executing.executingInterface as interface
import flows.deposit.handler
class DepositExecute(interface.ExecutingInterface):

    async def execute(self  ,query ,  **kwargs):
        await flows.deposit.handler.handler(query , kwargs.get('user_id'))

    