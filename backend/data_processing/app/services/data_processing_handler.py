from typing import Any
# Import the interface to ensure this class adheres to the contract
from ..services.I_data_processing_handler import IDataPreprocessingHandler

class DataProcessingHandler(IDataPreprocessingHandler):
    """
    Base implementation of the handler interface.
    Manages the linking of the chain elements.
    """
    def __init__(self):
        # Initialize the next handler as None
        self._next_handler: IDataPreprocessingHandler | None = None

    def set_next(self, handler: IDataPreprocessingHandler) -> IDataPreprocessingHandler:
        """
        Sets the next handler in the sequence and returns it to allow method chaining.
        """
        self._next_handler = handler
        return handler

    async def handle(self, data: Any, strategy: str) -> Any:
        """
        Default handling logic:
        If a next handler exists, delegate the request to it.
        Otherwise, return the data as is (end of chain).
        """
        if self._next_handler:
            return await self._next_handler.handle(data, strategy)
        return data