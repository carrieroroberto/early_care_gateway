# Import Abstract Base Class module
from abc import ABC, abstractmethod
from typing import Sequence
# Import the Report model
from ..models.report_model import Report

class IReportRepository(ABC):
    """
    Interface defining the contract for Report data access.
    """
    @abstractmethod
    async def find_by_patient_hashed_cf(self, patient_hashed_cf: str) -> Sequence[Report]:
        """
        Abstract method to find reports for a specific patient.
        """
        pass

    @abstractmethod
    async def find_by_doctor_id(self, doctor_id: int) -> Sequence[Report]:
        """
        Abstract method to find reports created by a specific doctor.
        """
        pass

    @abstractmethod
    async def save(self, report: Report) -> Report:
        """
        Abstract method to save a new report.
        """
        pass