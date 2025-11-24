from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .i_log_repository import ILogRepository
from ..models.log_model import Log

class LogRepository(ILogRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_doctor_id(self, doctor_id: int) -> List[Log] | None:
        result = await self.session.execute(select(Log).where(Log.doctor_id == doctor_id))
        logs = result.scalars().all()
        return logs if logs else None

    async def find_by_patient_cf(self, patient_cf: str) -> List[Log] | None:
        result = await self.session.execute(select(Log).where(Log.patient_hashed_cf == patient_cf))
        logs = result.scalars().all()
        return logs if logs else None

    async def save(self, log: Log) -> Log:
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log