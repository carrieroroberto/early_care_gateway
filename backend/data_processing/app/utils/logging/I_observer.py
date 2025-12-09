from abc import ABC, abstractmethod
from typing import Any, Dict

class IObserver(ABC):
    @abstractmethod
    async def update(self, payload: Dict[str, Any]):
        pass