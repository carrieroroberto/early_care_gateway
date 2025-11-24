from fastapi import APIRouter, Depends, HTTPException
from ..schemas.log_schema import LogRequest, LogResponse
from ..utils.dependencies import get_audit_service
from ..services.audit_service import AuditService

router = APIRouter(prefix="/audit", tags=["Endpoints"])

@router.post("/log", response_model=LogResponse)
async def log(
    log_request: LogRequest,
    service: AuditService = Depends(get_audit_service)
) -> LogResponse:
    try:
        return await service.log(log_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))