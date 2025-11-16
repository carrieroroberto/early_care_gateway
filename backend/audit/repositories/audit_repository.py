from abc import ABC, abstractmethod
from ..models.audit_model import LogEntry

class ILogRepository(ABC):
    @abstractmethod
    def save(self, log_entry: LogEntry):
        pass

class LogRepositoryImpl(ILogRepository):
    def __init__(self):
        self._db = []  # lista mock DB

    def save(self, log_entry: LogEntry):
        self._db.append(log_entry)
        print(f"[DB] Log saved: {log_entry}")
        return log_entry