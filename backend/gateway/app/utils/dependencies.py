# Import FastAPI components for handling headers and HTTP exceptions
from fastapi import Header, HTTPException
# Import the Gateway service and the custom HttpClient utility
from ..services.gateway_service import Gateway
from ..utils.http_client import HttpClient

# Initialize a single instance of HttpClient to be reused
http_client = HttpClient()
# Initialize the Gateway service, injecting the http_client dependency
gateway = Gateway(http_client=http_client)

async def get_gateway_service() -> Gateway:
    """
    Dependency function to provide the Gateway service instance.
    This allows FastAPI to inject the service into route handlers.
    """
    return gateway

async def get_jwt(authorization: str = Header(...)) -> str:
    """
    Dependency function to extract the JWT token from the Authorization header.
    Validates that the header starts with 'Bearer '.
    """
    # Check if the Authorization header has the correct "Bearer <token>" format
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid Authorization header")

    # Split the header string and return the token part
    return authorization.split(" ")[1]