import httpx
from typing import Dict, Any
# Import the Observer interface
from .I_observer import IObserver
# Import the custom HttpClient wrapper
from ..http_client import HttpClient


class AuditClient(IObserver):
    """
    Concrete implementation of the IObserver interface.
    Acts as a client that forwards log events to the external Audit Service.
    """

    def __init__(self, audit_url: str, http_client: HttpClient):
        # Store the URL of the Audit Service and the HTTP client instance
        self.audit_url = audit_url
        self.http = http_client

    async def update(self, payload: Dict[str, Any]):
        """
        Called when an event occurs in the Authentication service.
        Sends the event data to the Audit Service via HTTP POST.
        """
        # Filter the payload to remove keys with None values to ensure clean JSON
        clean_payload = {k: v for k, v in payload.items() if v is not None}

        try:
            # Send the log data to the Audit Service's /log endpoint
            await self.http.request(
                "POST",
                f"{self.audit_url}/log",
                json=clean_payload
            )
        except Exception as e:
            # Log an error message to the console if the request fails
            # (Does not raise the exception to prevent blocking the main auth flow)
            print(f"Failed to send log to Audit Service: {e}")