# Import Abstract Base Class module
from abc import ABC, abstractmethod
from typing import Any, Dict

class IObserver(ABC):
    """
    Interface defining the Observer component in the Observer design pattern.
    Classes implementing this interface must define how to handle updates from the Subject.
    """
    @abstractmethod
    async def update(self, payload: Dict[str, Any]):
        """
        Asynchronous method called by the Subject when an event occurs.
        Receives a dictionary containing event details.
        """
        pass