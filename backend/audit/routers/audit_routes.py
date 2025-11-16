from fastapi import APIRouter, Depends
from ..utils.audit_di import get_audit_service
from ..services.audit_service import AuditService

router = APIRouter(prefix="/audit")

@router.post("/log")
def log_event(event_data: dict, service: AuditService = Depends(get_audit_service)):
    return service.log_event(event_data)