# Import FastAPI dependency marker
from fastapi import Depends
# Import SQLAlchemy AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
# Import local utilities and services
from .db_connection import get_session
from ..repositories.log_repository import LogRepository
from ..repositories.i_log_repository import ILogRepository
from ..services.audit_service import AuditService

async def get_audit_service(session: AsyncSession = Depends(get_session)) -> AuditService:
    """
    Dependency to construct and provide the AuditService instance.
    Injects the LogRepository with the active database session.
    """
    # Initialize the repository with the current session
    log_repository: ILogRepository = LogRepository(session=session)

    # Return the service instance with the repository injected
    return AuditService(log_repository=log_repository)