import httpx

class HttpClient:
    """
    A wrapper class for the asynchronous HTTP client (httpx).
    Handles request execution and centralized error management.
    """
    def __init__(self, timeout: int = 30):
        # Initialize the httpx AsyncClient with a specified timeout (default 30s)
        self.client = httpx.AsyncClient(timeout=timeout)

    async def request(self, method: str, url: str, json: dict | None = None):
        """
        Performs an asynchronous HTTP request using the specified method and URL.
        """
        try:
            # Execute the request
            resp = await self.client.request(method, url, json=json)
            # Raise an exception for 4xx/5xx status codes
            resp.raise_for_status()
            # Return the JSON response body
            return resp.json()
        except httpx.HTTPStatusError as e:
            # Handle specific HTTP error responses (e.g., 400 Bad Request)
            try:
                # Attempt to parse the error details from the response JSON
                error_content = e.response.json()
                if "detail" in error_content:
                    raise Exception(error_content["detail"])
                else:
                    raise Exception(str(error_content))
            except ValueError:
                # Fallback if the error response is not valid JSON
                raise Exception(e.response.text or str(e))
        except httpx.HTTPError as e:
            # Handle general HTTP errors (e.g., connection issues)
            raise Exception(f"HTTP request failed: {e}") from e