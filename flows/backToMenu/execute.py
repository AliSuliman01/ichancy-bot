import executing.executingInterface as interface
import flows.backToMenu.handler
class BackToMenuExecute(interface):

    async def execute(self  ,query ,  **kwargs):
        await flows.backToMenu.handler.handler(query , kwargs.get('username'))

    