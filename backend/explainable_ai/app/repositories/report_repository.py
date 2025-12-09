from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.report_model import Report
from ..repositories.I_report_repository import IReportRepository

class ReportRepository(IReportRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, report: Report) -> Report:
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report

    async def find_by_patient_hashed_cf(self, patient_hashed_cf: str) -> Sequence[Report]:
        result = await self.session.execute(
            select(Report).where(Report.patient_hashed_cf == patient_hashed_cf)
        )
        return result.scalars().all()

    async def find_by_doctor_id(self, doctor_id: int) -> Sequence[Report]:
        result = await self.session.execute(
            select(Report).where(Report.doctor_id == doctor_id)
        )
        return result.scalars().all()