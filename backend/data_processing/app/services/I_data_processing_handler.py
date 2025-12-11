# Enable forward references for type hinting (needed for the set_next method return type)
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class IDataPreprocessingHandler(ABC):
    """
    Interface for the Chain of Responsibility pattern.
    Defines the contract for all data preprocessing handlers.
    """
    @abstractmethod
    def set_next(self, handler: IDataPreprocessingHandler) -> IDataPreprocessingHandler:
        """
        Sets the next handler in the chain.
        """
        pass

    @abstractmethod
    async def handle(self, data: Any, strategy: str) -> Any:
        """
        Processes the data if the strategy matches, or passes it to the next handler.
        """
        pass