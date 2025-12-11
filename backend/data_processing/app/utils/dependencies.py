import os
# Import FastAPI dependency injection marker
from fastapi import Depends
# Import SQLAlchemy AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
# Import internal utilities and services
from ..utils.db_connection import get_session
from ..utils.http_client import HttpClient
from ..utils.logging.audit_client import AuditClient
from ..repositories.data_repository import ProcessedDataRepository
from ..repositories.I_data_repository import IProcessedDataRepository
from ..services.data_service import DataProcessingService

# Configuration for the external Audit Service URL
audit_url = os.getenv("AUDIT_URL", "http://audit_service:8000/audit")

# Initialize the HTTP client used for inter-service communication
http_client = HttpClient()
# Initialize the AuditClient (Observer) to send logs to the Audit Service
audit_client = AuditClient(audit_url=audit_url, http_client=http_client)

async def get_data_service(session: AsyncSession = Depends(get_session)) -> DataProcessingService:
    """
    Dependency to construct and provide the DataProcessingService instance.
    It injects the repository and attaches the audit observer.
    """
    # Create the repository implementation using the current database session
    data_repository: IProcessedDataRepository = ProcessedDataRepository(session=session)

    # Instantiate the service with the repository and http client
    data_service = DataProcessingService(data_repository=data_repository, http_client=http_client)

    # Attach the audit client as an observer to log service events
    data_service.attach(audit_client)

    return data_service