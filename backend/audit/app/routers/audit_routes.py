from fastapi import APIRouter, Depends, HTTPException, Query
from ..schemas.log_schema import CreateLogResponse, GetLogsByDoctorResponse, CreateLogRequest
from ..utils.dependencies import get_audit_service
from ..services.audit_service import AuditService

router = APIRouter(prefix="/audit", tags=["Endpoints"])

@router.post("/log", response_model=CreateLogResponse)
async def log(log_request: CreateLogRequest, service: AuditService = Depends(get_audit_service)) -> CreateLogResponse:
    try:
        return await service.log(log_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/logs", response_model=GetLogsByDoctorResponse)
async def get_logs_by_doctor(doctor_id: int = Query(..., ge=1), service: AuditService = Depends(get_audit_service)) -> GetLogsByDoctorResponse:
    try:
        return await service.get_logs_by_doctor(doctor_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))