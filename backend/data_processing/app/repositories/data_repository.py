from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.data_model import ProcessedData
from ..repositories.I_data_repository import IProcessedDataRepository

class ProcessedDataRepository(IProcessedDataRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, processed_data: ProcessedData) -> int:
        self.session.add(processed_data)
        await self.session.commit()
        await self.session.refresh(processed_data)
        return processed_data.id

    async def find_by_id(self, id: int) -> ProcessedData:
        result = await self.session.execute(
            select(ProcessedData).where(ProcessedData.id == id)
        )
        return result.scalar_one()