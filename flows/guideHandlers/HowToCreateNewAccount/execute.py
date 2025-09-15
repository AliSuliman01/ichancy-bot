import executing.executingInterface as interface
import flows.guideHandlers.HowToCreateNewAccount.handler
class HowToCreateNewAccountExecute(interface.ExecutingInterface):
    async def execute(self  ,query ,  **kwargs):
        await flows.guideHandlers.HowToCreateNewAccount.handler.handler(query)

    