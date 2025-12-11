# Import Abstract Base Class module
from abc import ABC, abstractmethod
# Import the ProcessedData model to type hint the return values
from ..models.data_model import ProcessedData

class IProcessedDataRepository(ABC):
    """
    Interface defining the contract for Processed Data repository.
    Abstracts the underlying database operations.
    """
    @abstractmethod
    async def find_by_id(self, id: int) -> ProcessedData:
        """
        Abstract method to retrieve processed data by its unique ID.
        """
        pass

    @abstractmethod
    async def save(self, report: ProcessedData) -> int:
        """
        Abstract method to save a processed data entry.
        Returns the ID of the saved record.
        """
        pass