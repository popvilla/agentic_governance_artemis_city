from abc import ABC, abstractmethod

class Agent(ABC):
    def __init__(self, name, config=None):
        self.name = name
        self.config = config or {}
        
    @abstractmethod
    def handle(self, request, memory):
        """
        Handle a request.
        
        Args:
            request (dict): The request object.
            memory (MemoryBus): The memory bus instance.
            
        Returns:
            str: Response content.
        """
        pass
