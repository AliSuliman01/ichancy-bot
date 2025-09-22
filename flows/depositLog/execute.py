import executing.executingInterface as interface
import flows.depositLog.handler
class DepositLogExecute(interface.ExecutingInterface):

    async def execute(self  ,query , **wargs):
        await flows.depositLog.handler.handler(query , context = wargs.get('context'))
    
    