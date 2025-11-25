import httpx
from typing import Dict, Any
from ..logging.I_observer import IObserver

class AuditClient(IObserver):
    def __init__(self, audit_url: str):
        self.audit_url = audit_url

    async def update(self, payload: Dict[str, Any]):
        clean_payload = {k: v for k, v in payload.items() if v is not None}

        async with httpx.AsyncClient() as client:
            try:
                await client.post(f"{self.audit_url}/log", json=clean_payload)
            except Exception as e:
                print(f"Audit logging failed: {e}")