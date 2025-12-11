# Import FastAPI components for routing, dependency injection, and error handling
from fastapi import APIRouter, Depends, HTTPException

# Import schemas (Pydantic models) for request and response validation
from ..schemas.doctor_schema import (
    RegisterDoctorRequest, RegisterDoctorResponse,
    LoginDoctorRequest, LoginDoctorResponse,
    ValidateTokenRequest, ValidateTokenResponse
)

# Import the dependency function to get the AuthenticationService instance
from ..utils.dependencies import get_auth_service

# Import the AuthenticationService class
from ..services.authentication_service import AuthenticationService

# Initialize the API router with a prefix and tags for documentation
router = APIRouter(prefix="/authentication", tags=["Endpoints"])

@router.post("/register", response_model=RegisterDoctorResponse)
async def register(
    register_request: RegisterDoctorRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> RegisterDoctorResponse:
    """
    Endpoint to register a new doctor.
    """
    try:
        # Delegate registration logic to the authentication service
        return await auth_service.register_doctor(register_request)
    except Exception as e:
        # Return a 400 Bad Request if registration fails
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginDoctorResponse)
async def login(
    login_request: LoginDoctorRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> LoginDoctorResponse:
    """
    Endpoint to authenticate a doctor and retrieve a token.
    """
    try:
        # Delegate login logic to the authentication service
        return await auth_service.login_doctor(login_request)
    except Exception as e:
        # Return a 401 Unauthorized if login fails (e.g., wrong credentials)
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/validate", response_model=ValidateTokenResponse)
async def validate(
    token_request: ValidateTokenRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> ValidateTokenResponse:
    """
    Endpoint to validate an existing token.
    Used by the Gateway to check if a request is authorized.
    """
    try:
        # Delegate token validation to the authentication service
        return await auth_service.validate_token(token_request)
    except Exception as e:
        # Return a 401 Unauthorized if the token is invalid or expired
        raise HTTPException(status_code=401, detail=str(e))