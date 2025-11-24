from fastapi import APIRouter, Depends, HTTPException
from ..schemas.doctor_schema import (
    RegisterDoctorRequest, RegisterDoctorResponse,
    LoginDoctorRequest, LoginDoctorResponse,
    ValidateTokenRequest, ValidateTokenResponse
)
from ..utils.dependencies import get_auth_service
from ..services.authentication_service import AuthenticationService

router = APIRouter(prefix="/authentication", tags=["Endpoints"])

@router.post("/register", response_model=RegisterDoctorResponse)
async def register(
    register_request: RegisterDoctorRequest,
    service: AuthenticationService = Depends(get_auth_service)
) -> RegisterDoctorResponse:
    try:
        return await service.register_doctor(register_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginDoctorResponse)
async def login(
    login_request: LoginDoctorRequest,
    service: AuthenticationService = Depends(get_auth_service)
) -> LoginDoctorResponse:
    try:
        return await service.login_doctor(login_request)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/validate", response_model=ValidateTokenResponse)
async def validate(
    token_request: ValidateTokenRequest,
    service: AuthenticationService = Depends(get_auth_service)
) -> ValidateTokenResponse:
    try:
        return await service.validate_token(token_request)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))