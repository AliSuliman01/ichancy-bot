import executing.executingInterface as interface
import flows.problemInBot.handler
class ProblemInBotExecute(interface.ExecutingInterface):

    async def execute(self , query , **kwargs):
        await flows.problemInBot.handler.handler(query)

    