import executing.executingInterface as interface
import flows.log.handler
class LogExecute(interface.ExecutingInterface):

    async def execute(self  ,query , **wargs):
        await flows.log.handler.handler(query)
    
    