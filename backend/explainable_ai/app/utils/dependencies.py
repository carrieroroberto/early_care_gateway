import os
# Import FastAPI dependency injection marker
from fastapi import Depends
# Import SQLAlchemy AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
# Import internal utilities and services
from ..utils.db_connection import get_session
from ..utils.http_client import HttpClient
from ..utils.logging.audit_client import AuditClient
from ..repositories.report_repository import ReportRepository
from ..repositories.I_report_repository import IReportRepository
from ..services.xai_service import XAiService

# Configuration for the external Audit Service URL
audit_url = os.getenv("AUDIT_URL", "http://audit_service:8000/audit")

# Initialize the HTTP client for inter-service communication
http_client = HttpClient()
# Initialize the AuditClient (Observer) to send logs to the Audit Service
audit_client = AuditClient(audit_url=audit_url, http_client=http_client)

async def get_xai_service(session: AsyncSession = Depends(get_session)) -> XAiService:
    """
    Dependency to construct and provide the XAiService instance.
    It injects the repository and attaches the audit observer.
    """
    # Create the repository implementation using the current database session
    report_repository: IReportRepository = ReportRepository(session=session)

    # Instantiate the service with the repository and http client
    xai_service = XAiService(reports_repository=report_repository, http_client=http_client)

    # Attach the audit client as an observer to log service events (e.g., analysis completed)
    xai_service.attach(audit_client)

    return xai_service