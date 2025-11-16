from ..repositories.audit_repository import LogRepositoryImpl
from ..services.audit_service import AuditService

log_repository = LogRepositoryImpl()
audit_service = AuditService(log_repository)

def get_audit_service() -> AuditService:
    return audit_service