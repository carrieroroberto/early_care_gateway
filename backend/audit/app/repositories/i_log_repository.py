from abc import ABC, abstractmethod
from typing import List
from ..models.log_model import Log

class ILogRepository(ABC):
    @abstractmethod
    async def find_by_doctor_id(self, id: int) -> List[Log] | None:
        pass

    @abstractmethod
    async def find_by_patient_cf(self, cf: str) -> List[Log] | None:
        pass

    @abstractmethod
    async def save(self, log: Log) -> Log:
        pass