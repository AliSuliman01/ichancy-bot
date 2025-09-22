import executing.executingInterface as interface
import flows.withdrawLog.handler
class WithdrawLogExecute(interface.ExecutingInterface):

    async def execute(self  ,query , **wargs):
        await flows.withdrawLog.handler.handler(query , context = wargs.get('context'))
    
    