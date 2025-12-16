import executing.executingInterface as interface
import flows.guideHandlers.guides.handler
class GuidesExecute(interface.ExecutingInterface):

    async def execute(self  ,query ,  **kwargs):
        await flows.guideHandlers.guides.handler.handler(query)

    