import executing.executingInterface as interface
import flows.approveDepositFromAdmin.handler
class ApproveDepositeFromAdmin(interface.ExecutingInterface):

    async def execute(self  ,query ,  **kwargs):
        await flows.approveDepositFromAdmin.handler.handler(query , kwargs.get('context') )
    
    