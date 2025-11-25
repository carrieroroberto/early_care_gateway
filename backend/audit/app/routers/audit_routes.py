from fastapi import APIRouter, Depends, HTTPException, Query
from ..schemas.log_schema import CreateLogResponse, CreateLogRequest, GetLogsResponse, GetLogsRequest
from ..utils.dependencies import get_audit_service
from ..services.audit_service import AuditService

router = APIRouter(prefix="/audit", tags=["Endpoints"])

@router.post("/log", response_model=CreateLogResponse)
async def log(log_request: CreateLogRequest, audit_service: AuditService = Depends(get_audit_service)) -> CreateLogResponse:
    try:
        return await audit_service.log(log_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/logs", response_model=GetLogsResponse)
async def get_logs(
    get_logs_request: GetLogsRequest = Depends(), audit_service: AuditService = Depends(get_audit_service)) -> GetLogsResponse:
    try:
        logs = await audit_service.get_logs(get_logs_request)
        return logs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))