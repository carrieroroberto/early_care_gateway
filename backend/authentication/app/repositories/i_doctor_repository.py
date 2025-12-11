# Import Abstract Base Class module to define the interface
from abc import ABC, abstractmethod
# Import the Doctor model
from ..models.doctor_model import Doctor

class IDoctorRepository(ABC):
    """
    Interface defining the contract for Doctor data access operations.
    Implementing classes must provide concrete logic for these methods.
    """

    @abstractmethod
    async def find_by_id(self, id: int) -> Doctor | None:
        """
        Abstract method to retrieve a doctor by their unique ID.
        """
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Doctor | None:
        """
        Abstract method to retrieve a doctor by their email address.
        """
        pass

    @abstractmethod
    async def save(self, doctor: Doctor) -> Doctor:
        """
        Abstract method to save (create or update) a doctor entity.
        """
        pass