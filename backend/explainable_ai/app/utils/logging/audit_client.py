import httpx
from typing import Dict, Any
# Import the Observer interface
from .I_observer import IObserver
# Import the HttpClient wrapper
from ..http_client import HttpClient


class AuditClient(IObserver):
    """
    Concrete implementation of the IObserver interface.
    Responsible for forwarding log events to the external Audit Service.
    """

    def __init__(self, audit_url: str, http_client: HttpClient):
        # Store the Audit Service URL and the HTTP client instance
        self.audit_url = audit_url
        self.http = http_client

    async def update(self, payload: Dict[str, Any]):
        """
        Handles the update notification from the Subject.
        Sends the event payload to the Audit Service via HTTP POST.
        """
        # Clean the payload by removing keys with None values
        clean_payload = {k: v for k, v in payload.items() if v is not None}

        try:
            # Send the log to the Audit Service
            await self.http.request(
                "POST",
                f"{self.audit_url}/log",
                json=clean_payload
            )
        except Exception as e:
            # Log failure to console without breaking the main application flow
            print(f"Failed to send log to Audit Service: {e}")