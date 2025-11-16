from fastapi import APIRouter, Depends, HTTPException
from ..utils.dependecy_injection import get_auth_service
from ..services.authentication_service import AuthenticationService

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(email: str, password: str, 
             service: AuthenticationService = Depends(get_auth_service)):
    return service.registerUser(email, password)

@router.post("/login")
def login(email: str, password: str,
          service: AuthenticationService = Depends(get_auth_service)):
    return {"token": service.loginUser(email, password)}

@router.get("/validate")
def validate(token: str,
             service: AuthenticationService = Depends(get_auth_service)):
    return {"user_id": service.validateToken(token)}