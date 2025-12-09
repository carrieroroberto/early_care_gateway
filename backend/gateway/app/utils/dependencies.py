from fastapi import Header, HTTPException
from ..services.gateway_service import Gateway
from ..utils.http_client import HttpClient

http_client = HttpClient()
gateway = Gateway(http_client=http_client)

async def get_gateway_service() -> Gateway:
    return gateway

async def get_jwt(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid Authorization header")

    return authorization.split(" ")[1]