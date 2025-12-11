# Import SQLAlchemy AsyncSession for database interactions
from sqlalchemy.ext.asyncio import AsyncSession
# Import select for building queries
from sqlalchemy import select
# Import the model and the repository interface
from ..models.data_model import ProcessedData
from ..repositories.I_data_repository import IProcessedDataRepository

class ProcessedDataRepository(IProcessedDataRepository):
    """
    Concrete implementation of the IProcessedDataRepository.
    Handles direct database operations using SQLAlchemy.
    """
    def __init__(self, session: AsyncSession):
        # Inject the database session
        self.session = session

    async def save(self, processed_data: ProcessedData) -> int:
        """
        Saves a ProcessedData instance to the database.
        """
        # Add the object to the session
        self.session.add(processed_data)
        # Commit the transaction
        await self.session.commit()
        # Refresh the instance to get the generated ID
        await self.session.refresh(processed_data)
        return processed_data.id

    async def find_by_id(self, id: int) -> ProcessedData:
        """
        Retrieves a ProcessedData record by its ID.
        """
        # Execute a SELECT query filtered by ID
        result = await self.session.execute(
            select(ProcessedData).where(ProcessedData.id == id)
        )
        # Return the single result or raise an error if not found
        return result.scalar_one()