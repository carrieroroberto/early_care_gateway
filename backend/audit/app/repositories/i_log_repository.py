from abc import ABC, abstractmethod
from typing import Sequence
from ..models.log_model import Log

class ILogRepository(ABC):

    @abstractmethod
    async def save(self, log: Log) -> Log:
        pass

    @abstractmethod
    async def find_all(self) -> Sequence[Log]:
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
        pass