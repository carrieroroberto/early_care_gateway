from fastapi import APIRouter, Depends, HTTPException
from ..utils.dependencies import get_auth_service
from ..services.authentication_service import AuthenticationService

router = APIRouter(prefix="/authentication", tags=["Authentication"])

@router.post("/register")
async def register(
    name: str,
    surname: str,
    email: str,
    password: str,
    service: AuthenticationService = Depends(get_auth_service)
):
    try:
        doctor = await service.registerDoctor(name, surname, email, password)
        return {"message": "Doctor registered successfully", "doctor_id": doctor.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(
    email: str,
    password: str,
    service: AuthenticationService = Depends(get_auth_service)
):
    try:
        token = await service.loginDoctor(email, password)
        return {"jwt_token": token}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/validate")
async def validate(
    token: str,
    service: AuthenticationService = Depends(get_auth_service)
):
    try:
        doctor_id = await service.validateToken(token)
        return {"doctor_id": doctor_id}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))