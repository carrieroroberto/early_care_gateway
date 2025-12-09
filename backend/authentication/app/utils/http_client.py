import httpx

class HttpClient:
    def __init__(self, timeout: int = 30):
        self.client = httpx.AsyncClient(timeout=timeout)

    async def request(self, method: str, url: str, json: dict | None = None):
        try:
            resp = await self.client.request(method, url, json=json)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            try:
                error_content = e.response.json()
                if "detail" in error_content:
                    raise Exception(error_content["detail"])
                else:
                    raise Exception(str(error_content))
            except ValueError:
                raise Exception(e.response.text or str(e))
        except httpx.HTTPError as e:
            print(f"HTTP Request failed: {e}")
            raise