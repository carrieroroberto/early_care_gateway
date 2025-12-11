import httpx
from typing import Dict, Any
# Import the Observer interface
from .I_observer import IObserver
# Import the HttpClient wrapper
from ..http_client import HttpClient


class AuditClient(IObserver):
    """
    Concrete implementation of the IObserver interface.
    Responsible for sending log events to the external Audit Service.
    """

    def __init__(self, audit_url: str, http_client: HttpClient):
        # Store the Audit Service URL and the HTTP client instance
        self.audit_url = audit_url
        self.http = http_client

    async def update(self, payload: Dict[str, Any]):
        """
        Handles the update notification from the Subject.
        Sends the payload to the Audit Service via an HTTP POST request.
        """
        # Filter out keys with None values to ensure the JSON payload is clean
        clean_payload = {k: v for k, v in payload.items() if v is not None}

        try:
            # Perform the POST request to the audit log endpoint
            await self.http.request(
                "POST",
                f"{self.audit_url}/log",
                json=clean_payload
            )
        except Exception as e:
            # Catch and log any errors that occur during the logging process.
            # We avoid raising the exception to prevent the main application flow from breaking.
            print(f"Failed to send log to Audit Service: {e}")