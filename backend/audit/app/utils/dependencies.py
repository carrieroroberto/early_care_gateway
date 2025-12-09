from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .db_connection import get_session
from ..repositories.log_repository import LogRepository
from ..repositories.i_log_repository import ILogRepository
from ..services.audit_service import AuditService

async def get_audit_service(session: AsyncSession = Depends(get_session)) -> AuditService:
    log_repository: ILogRepository = LogRepository(session=session)

    return AuditService(log_repository=log_repository)