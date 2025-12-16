import executing.executingInterface as interface
import flows.messageToAdmin.handler
class MessageToAdminExecute(interface.ExecutingInterface):

    async def execute(self , query , **kwargs):
        await flows.messageToAdmin.handler.handler()

    