from typing import Sequence
# Import SQLAlchemy AsyncSession and query constructs
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
# Import the interface and model
from .i_log_repository import ILogRepository
from ..models.log_model import Log


class LogRepository(ILogRepository):
    """
    Concrete implementation of the ILogRepository using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        # Inject the database session
        self.session = session

    async def save(self, log: Log) -> Log:
        """
        Persists a Log object to the database.
        """
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def find_all(self) -> Sequence[Log]:
        """
        Retrieves all records from the logs table.
        """
        result = await self.session.execute(select(Log))
        # Return all scalars (Log objects)
        return result.scalars().all()

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
        Dynamically builds a query to find logs based on provided non-null filters.
        """
        conditions = []

        # Add conditions for each filter provided
        if service is not None:
            conditions.append(Log.service == service)
        if event is not None:
            conditions.append(Log.event == event)
        if doctor_id is not None:
            conditions.append(Log.doctor_id == doctor_id)
        if patient_hashed_cf is not None:
            conditions.append(Log.patient_hashed_cf == patient_hashed_cf)
        if report_id is not None:
            conditions.append(Log.report_id == report_id)
        if data_id is not None:
            conditions.append(Log.data_id == data_id)

        # Start building the query
        query = select(Log)

        # Apply the AND operator to all collected conditions
        if conditions:
            query = query.where(and_(*conditions))

        # Execute the query and return results
        result = await self.session.execute(query)
        return result.scalars().all()