import os
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.db_connection import get_session
from ..utils.http_client import HttpClient
from ..utils.logging.audit_client import AuditClient
from ..repositories.report_repository import ReportRepository
from ..repositories.I_report_repository import IReportRepository
from ..services.xai_service import XAiService

audit_url = os.getenv("AUDIT_URL", "http://audit_service:8000/audit")
http_client = HttpClient()
audit_client = AuditClient(audit_url=audit_url, http_client=http_client)

async def get_xai_service(session: AsyncSession = Depends(get_session)) -> XAiService:
    report_repository: IReportRepository = ReportRepository(session=session)

    xai_service = XAiService(reports_repository=report_repository, http_client=http_client)

    xai_service.attach(audit_client)

    return xai_service