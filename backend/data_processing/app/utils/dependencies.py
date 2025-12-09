import os
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.db_connection import get_session
from ..utils.http_client import HttpClient
from ..utils.logging.audit_client import AuditClient
from ..repositories.data_repository import ProcessedDataRepository
from ..repositories.I_data_repository import IProcessedDataRepository
from ..services.data_service import DataProcessingService

audit_url = os.getenv("AUDIT_URL", "http://audit_service:8000/audit")
http_client = HttpClient()
audit_client = AuditClient(audit_url=audit_url, http_client=http_client)

async def get_data_service(session: AsyncSession = Depends(get_session)) -> DataProcessingService:
    data_repository: IProcessedDataRepository = ProcessedDataRepository(session=session)

    data_service = DataProcessingService(data_repository=data_repository, http_client=http_client)

    data_service.attach(audit_client)

    return data_service