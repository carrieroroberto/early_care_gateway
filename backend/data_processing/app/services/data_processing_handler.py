from typing import Any
from ..services.I_data_processing_handler import IDataPreprocessingHandler

class DataProcessingHandler(IDataPreprocessingHandler):
    def __init__(self):
        self._next_handler: IDataPreprocessingHandler | None = None

    def set_next(self, handler: IDataPreprocessingHandler) -> IDataPreprocessingHandler:
        self._next_handler = handler
        return handler

    async def handle(self, data: Any, strategy: str) -> Any:
        if self._next_handler:
            return await self._next_handler.handle(data, strategy)
        return data