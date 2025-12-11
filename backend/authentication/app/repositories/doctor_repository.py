# Import AsyncSession for asynchronous database interactions
from sqlalchemy.ext.asyncio import AsyncSession
# Import 'select' construct for building queries
from sqlalchemy import select
# Import the interface to ensure this class adheres to the contract
from .i_doctor_repository import IDoctorRepository
# Import the Doctor model
from ..models.doctor_model import Doctor

class DoctorRepository(IDoctorRepository):
    """
    Concrete implementation of the IDoctorRepository using SQLAlchemy.
    """
    def __init__(self, session: AsyncSession):
        # Inject the asynchronous database session
        self.session = session

    async def find_by_id(self, id: int) -> Doctor | None:
        """
        Retrieves a doctor record by ID using a SELECT query.
        Returns None if no record is found.
        """
        # Build the query: SELECT * FROM doctors WHERE id = :id
        stmt = select(Doctor).where(Doctor.id == id)
        # Execute the query
        result = await self.session.execute(stmt)
        # Return the single scalar result or None
        return result.scalar_one_or_none()

    async def find_by_email(self, email: str) -> Doctor | None:
        """
        Retrieves a doctor record by email.
        """
        # Build the query: SELECT * FROM doctors WHERE email = :email
        stmt = select(Doctor).where(Doctor.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save(self, doctor: Doctor) -> Doctor:
        """
        Persists a Doctor object to the database.
        """
        # Add the instance to the session
        self.session.add(doctor)
        # Commit the transaction to save changes to the DB
        await self.session.commit()
        # Refresh the instance to update attributes (e.g., getting the auto-generated ID)
        await self.session.refresh(doctor)
        return doctor