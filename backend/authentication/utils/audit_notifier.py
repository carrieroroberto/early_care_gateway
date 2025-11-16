from abc import ABC, abstractmethod

class IAuditNotifier(ABC):
    @abstractmethod
    def notify(self, eventType: str, details: dict):
        pass

class AuditClient(IAuditNotifier):
    def notify(self, eventType: str, details: dict):
        print(f"[AUDIT] {eventType} -> {details}")