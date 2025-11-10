import executing.executingInterface as interface
import flows.referalDetails.handler
class ReferalDetailsExecute(interface.ExecutingInterface):

    async def execute(self , query , **kwargs):
        await flows.referalDetails.handler.handler(query)

    