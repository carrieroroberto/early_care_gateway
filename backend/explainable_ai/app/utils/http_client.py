import httpx

class HttpClient:
    """
    A wrapper class around httpx.AsyncClient to handle HTTP requests.
    Provides centralized error handling and timeout configuration.
    """
    def __init__(self, timeout: int = 30):
        # Initialize the client with a default timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def request(self, method: str, url: str, json: dict | None = None):
        """
        Executes an asynchronous HTTP request.
        """
        try:
            # Perform the request
            resp = await self.client.request(method, url, json=json)
            # Raise an exception for 4xx/5xx status codes
            resp.raise_for_status()
            # Return the JSON response body
            return resp.json()
        except httpx.HTTPStatusError as e:
            # Handle specific HTTP error responses
            try:
                error_content = e.response.json()
                if "detail" in error_content:
                    raise Exception(error_content["detail"])
                else:
                    raise Exception(str(error_content))
            except ValueError:
                # Fallback if the error response is not valid JSON
                raise Exception(e.response.text or str(e))
        except httpx.HTTPError as e:
            # Handle general network or connection errors
            raise Exception(f"HTTP request failed: {e}") from e