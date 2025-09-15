import executing.executingInterface as interface
import flows.startFlow.handler
class StartFlowExecute(interface.ExecutingInterface):
    async def execute(self , query , **kwargs):
        await flows.startFlow.handler.handler()

    