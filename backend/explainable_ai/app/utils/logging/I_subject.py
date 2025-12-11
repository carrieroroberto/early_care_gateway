# Import Abstract Base Class module
from abc import ABC, abstractmethod
from typing import Any, Dict
# Import the Observer interface
from ..logging.I_observer import IObserver

class ISubject(ABC):
    """
    Interface defining the Subject component in the Observer design pattern.
    The Subject maintains a list of dependents (observers) and notifies them of events.
    """
    @abstractmethod
    def attach(self, observer: IObserver):
        """
        Method to attach (subscribe) an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: IObserver):
        """
        Method to detach (unsubscribe) an observer from the subject.
        """
        pass

    @abstractmethod
    async def notify(self, payload: Dict[str, Any]):
        """
        Asynchronous method to notify all attached observers of an event.
        """
        pass