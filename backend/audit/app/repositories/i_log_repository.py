# Import Abstract Base Class module
from abc import ABC, abstractmethod
from typing import Sequence
# Import the Log model
from ..models.log_model import Log

class ILogRepository(ABC):
    """
    Interface defining the contract for Log repository operations.
    """

    @abstractmethod
    async def save(self, log: Log) -> Log:
        """
        Abstract method to save a new log entry.
        """
        pass

    @abstractmethod
    async def find_all(self) -> Sequence[Log]:
        """
        Abstract method to retrieve all logs.
        """
        pass

    @abstractmethod
    async def find_with_filters(
        self,
        service: str | None = None,
        event: str | None = None,
        doctor_id: int | None = None,
        patient_hashed_cf: str | None = None,
        report_id: int | None = None,
        data_id: int | None = None
    ) -> Sequence[Log]:
        """
        Abstract method to retrieve logs matching specific criteria.
        """
        pass