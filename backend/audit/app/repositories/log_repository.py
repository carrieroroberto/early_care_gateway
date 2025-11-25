from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from .i_log_repository import ILogRepository
from ..models.log_model import Log

class LogRepository(ILogRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, log: Log) -> Log:
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def find_all(self) -> Sequence[Log]:
        result = await self.session.execute(select(Log))
        return result.scalars().all()   # sempre una Sequence, mai None

    async def find_with_filters(
        self,
        service: str | None = None,
        event: str | None = None,
        doctor_id: int | None = None,
        patient_hashed_cf: str | None = None,
        report_id: int | None = None,
        data_id: int | None = None
    ) -> Sequence[Log]:

        conditions = []
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

        query = select(Log)
        if conditions:
            query = query.where(and_(*conditions))

        result = await self.session.execute(query)
        return result.scalars().all()