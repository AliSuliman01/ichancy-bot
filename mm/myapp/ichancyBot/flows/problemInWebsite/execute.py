import executing.executingInterface as interface
import flows.problemInWebsite.handler
class ProblemInWebsiteExecute(interface.ExecutingInterface):

    async def execute(self , query , **kwargs):
        await flows.problemInWebsite.handler.handler(query)

    