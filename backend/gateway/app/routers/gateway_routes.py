from fastapi import APIRouter, Depends, HTTPException, Query
from ..schemas.auth_schema import RegisterResponse, RegisterRequest, LoginResponse, LoginRequest
from ..schemas.xai_schema import AnalyseResponse, AnalyseRequest, GetReportsResponse
from ..utils.dependencies import get_gateway_service, get_jwt
from ..services.gateway_service import Gateway

router = APIRouter(prefix="/gateway", tags=["Endpoints"])

@router.post("/register", response_model=RegisterResponse)
async def register(register_body: RegisterRequest, gateway_service: Gateway = Depends(get_gateway_service)) -> RegisterResponse:
    try:
        return await gateway_service.register(register_body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=LoginResponse)
async def login(login_body: LoginRequest, gateway_service: Gateway = Depends(get_gateway_service)) -> LoginResponse:
    try:
        return await gateway_service.login(login_body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyse", response_model=AnalyseResponse)
async def analyse(
    analyse_body: AnalyseRequest, jwt: str = Depends(get_jwt), gateway_service: Gateway = Depends(get_gateway_service)) -> AnalyseResponse:
    try:
        return await gateway_service.analyse(jwt=jwt, analyse_request=analyse_body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reports", response_model=GetReportsResponse)
async def get_reports(jwt: str = Depends(get_jwt), patient_hashed_cf: str | None = Query(None), gateway_service: Gateway = Depends(get_gateway_service)) -> GetReportsResponse:
    try:
        return await gateway_service.get_reports(jwt=jwt, patient_hashed_cf=patient_hashed_cf)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))