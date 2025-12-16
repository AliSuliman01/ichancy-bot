import executing.executingInterface as interface
import flows.contactUs.handler
class ContactUsExecute(interface.ExecutingInterface):

    async def execute(self , query , **kwargs):
        await flows.contactUs.handler.handler(query)

    