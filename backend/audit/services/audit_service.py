from ..repositories.audit_repository import ILogRepository
from ..models.audit_model import LogEntry

class AuditService:
    def __init__(self, log_repository: ILogRepository):
        self.log_repository = log_repository

    def log_event(self, event_data: dict):
        log_entry = LogEntry(
            event_type=event_data.get("event_type", "UNKNOWN"),
            details=event_data
        )
        return self.log_repository.save(log_entry)