import executing.executingInterface as interface
import flows.approveWithdrawFromAdmin.handler
class ApproveWithdrawFromAdmin(interface.ExecutingInterface):

    async def execute(self  ,query ,  **kwargs):
        await flows.approveWithdrawFromAdmin.handler.handler(query , kwargs.get('context') )
    
    