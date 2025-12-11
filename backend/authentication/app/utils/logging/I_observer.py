# Import Abstract Base Class module to define the interface
from abc import ABC, abstractmethod
from typing import Any, Dict

class IObserver(ABC):
    """
    Interface defining the Observer component in the Observer design pattern.
    Classes implementing this interface must define the 'update' method.
    """
    @abstractmethod
    async def update(self, payload: Dict[str, Any]):
        """
        Asynchronous method called by the Subject to notify the Observer of an event.
        """
        pass