from abc import ABC, abstractmethod
from typing import Any, Dict
from ..logging.I_observer import IObserver

class ISubject(ABC):
    @abstractmethod
    def attach(self, observer: IObserver):
        pass

    @abstractmethod
    def detach(self, observer: IObserver):
        pass

    @abstractmethod
    async def notify(self, payload: Dict[str, Any]):
        pass