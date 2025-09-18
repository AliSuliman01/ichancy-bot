import executing.executingInterface as interface
import flows.rejectDepositFromAdmin.handler
class RejectDepositeFromAdmin(interface.ExecutingInterface):

    async def execute(self  ,query ,  **kwargs):
        await flows.rejectDepositFromAdmin.handler.handler(query , kwargs.get('context') )
    
    