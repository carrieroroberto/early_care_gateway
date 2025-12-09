import httpx
from typing import Dict, Any
from .I_observer import IObserver
from ..http_client import HttpClient

class AuditClient(IObserver):
    def __init__(self, audit_url: str, http_client: HttpClient):
        self.audit_url = audit_url
        self.http = http_client

    async def update(self, payload: Dict[str, Any]):
        clean_payload = {k: v for k, v in payload.items() if v is not None}
        
        try:
            await self.http.request(
                "POST",
                f"{self.audit_url}/log",
                json=clean_payload
            )
        except Exception as e:
            print(f"Failed to send log to Audit Service: {e}")