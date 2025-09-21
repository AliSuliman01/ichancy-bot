import executing.executingInterface as interface
import flows.referal.handler
class ReferalExecute(interface.ExecutingInterface):

    async def execute(self , query , **kwargs):
        await flows.referal.handler.handler(query)

    