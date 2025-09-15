from abc import ABC , abstractmethod



class ExecutingInterface(ABC):
     @abstractmethod
     async def execute(self , query , **kwargs):
        pass
    
