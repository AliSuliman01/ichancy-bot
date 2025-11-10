import executing.executingInterface as interface
import flows.terms.handler
class TermsExecute(interface.ExecutingInterface):
      async def execute(self , query , **kwargs):
         await flows.terms.handler.handler(query)
