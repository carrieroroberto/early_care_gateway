# Import Abstract Base Class module
from abc import ABC, abstractmethod
from typing import Any, Dict
# Import the IObserver interface
from ..logging.I_observer import IObserver

class ISubject(ABC):
    """
    Interface defining the Subject component in the Observer design pattern.
    The Subject maintains a list of dependents (observers) and notifies them of state changes.
    """
    @abstractmethod
    def attach(self, observer: IObserver):
        """
        Registers an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: IObserver):
        """
        Unregisters an observer from the subject.
        """
        pass

    @abstractmethod
    async def notify(self, payload: Dict[str, Any]):
        """
        Notifies all registered observers about an event, passing the event data.
        """
        pass