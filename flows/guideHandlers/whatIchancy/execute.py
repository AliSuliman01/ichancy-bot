import executing.executingInterface as interface
import flows.guideHandlers.whatIchancy.handler
class WhatIchancyExecute(interface):
    async def execute(self  ,query ,  **kwargs):
        await flows.guideHandlers.whatIchancy.handler.handler(query)

    