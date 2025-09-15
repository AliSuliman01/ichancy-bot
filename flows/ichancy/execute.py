import executing.executingInterface as interface
import flows.ichancy.handler
class IchancyExecute(interface.ExecutingInterface):
    async def execute(self , query , **kwargs):
        await flows.ichancy.handler.handler(query , kwargs.get('user_id'))

    