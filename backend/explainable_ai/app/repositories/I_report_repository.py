from abc import ABC, abstractmethod
from typing import Sequence
from ..models.report_model import Report

class IReportRepository(ABC):
    @abstractmethod
    async def find_by_patient_hashed_cf(self, patient_hashed_cf: str) -> Sequence[Report]:
        pass

    @abstractmethod
    async def find_by_doctor_id(self, doctor_id: int) -> Sequence[Report]:
        pass

    @abstractmethod
    async def save(self, report: Report) -> Report:
        pass