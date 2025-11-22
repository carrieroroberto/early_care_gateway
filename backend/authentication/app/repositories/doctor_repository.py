from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.doctor_model import Doctor

class DoctorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, id: int):
        stmt = select(Doctor).where(Doctor.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_email(self, email: str):
        stmt = select(Doctor).where(Doctor.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save(self, doctor: Doctor):
        self.session.add(doctor)
        await self.session.commit()
        await self.session.refresh(doctor)
        return doctor