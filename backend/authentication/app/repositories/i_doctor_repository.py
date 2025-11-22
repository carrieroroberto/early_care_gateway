from abc import ABC, abstractmethod
from ..models.doctor_model import Doctor

class IDoctorRepository(ABC):

    @abstractmethod
    async def find_by_id(self, id: int) -> Doctor | None:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Doctor | None:
        pass

    @abstractmethod
    async def save(self, doctor: Doctor) -> Doctor:
        pass