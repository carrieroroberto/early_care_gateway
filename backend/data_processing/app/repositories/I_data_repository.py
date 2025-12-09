from abc import ABC, abstractmethod
from ..models.data_model import ProcessedData

class IProcessedDataRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: int) -> ProcessedData:
        pass

    @abstractmethod
    async def save(self, report: ProcessedData) -> int:
        pass