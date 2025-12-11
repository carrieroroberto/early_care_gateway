import httpx

class HttpClient:
    """
    A wrapper around httpx.AsyncClient to handle HTTP requests.
    Includes centralized error handling.
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
            # Raise an exception if the status code indicates an error (4xx or 5xx)
            resp.raise_for_status()
            # Return the parsed JSON response
            return resp.json()
        except httpx.HTTPStatusError as e:
            # Handle specific HTTP errors returned by the server
            try:
                error_content = e.response.json()
                # Extract error detail if available
                if "detail" in error_content:
                    raise Exception(error_content["detail"])
                else:
                    raise Exception(str(error_content))
            except ValueError:
                # Fallback if response is not valid JSON
                raise Exception(e.response.text or str(e))
        except httpx.HTTPError as e:
            # Handle general network or connection errors
            print(f"HTTP Request failed: {e}")
            raise