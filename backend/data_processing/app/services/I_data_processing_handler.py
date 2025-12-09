from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class IDataPreprocessingHandler(ABC):
    @abstractmethod
    def set_next(self, handler: IDataPreprocessingHandler) -> IDataPreprocessingHandler:
        pass

    @abstractmethod
    async def handle(self, data: Any, strategy: str) -> Any:
        pass