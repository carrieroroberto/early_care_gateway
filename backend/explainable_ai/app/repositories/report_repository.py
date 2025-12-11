from typing import Sequence
# Import SQLAlchemy AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
# Import select construct
from sqlalchemy import select
# Import the model and interface
from ..models.report_model import Report
from ..repositories.I_report_repository import IReportRepository

class ReportRepository(IReportRepository):
    """
    Concrete implementation of the IReportRepository.
    """
    def __init__(self, session: AsyncSession):
        # Inject the database session
        self.session = session

    async def save(self, report: Report) -> Report:
        """
        Saves a report to the database.
        """
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def find_by_patient_hashed_cf(self, patient_hashed_cf: str) -> Sequence[Report]:
        """
        Retrieves all reports associated with a specific patient's hashed fiscal code.
        """
        # Execute SELECT query filtering by patient_hashed_cf
        result = await self.session.execute(
            select(Report).where(Report.patient_hashed_cf == patient_hashed_cf)
        )
        # Return all matching records
        return result.scalars().all()

    async def find_by_doctor_id(self, doctor_id: int) -> Sequence[Report]:
        """
        Retrieves all reports created by a specific doctor.
        """
        # Execute SELECT query filtering by doctor_id
        result = await self.session.execute(
            select(Report).where(Report.doctor_id == doctor_id)
        )
        return result.scalars().all()