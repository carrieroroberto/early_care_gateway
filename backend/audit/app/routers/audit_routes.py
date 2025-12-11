# Import FastAPI components for routing, dependency injection, and HTTP exceptions
from fastapi import APIRouter, Depends, HTTPException, Query

# Import Pydantic schemas for log creation and retrieval
from ..schemas.log_schema import CreateLogResponse, CreateLogRequest, GetLogsResponse, GetLogsRequest

# Import dependency function to get the Audit service instance
from ..utils.dependencies import get_audit_service

# Import the Audit service class
from ..services.audit_service import AuditService

# Initialize the router with a prefix for audit endpoints
router = APIRouter(prefix="/audit", tags=["Endpoints"])

@router.post("/log", response_model=CreateLogResponse)
async def log(log_request: CreateLogRequest, audit_service: AuditService = Depends(get_audit_service)) -> CreateLogResponse:
    """
    Endpoint to create a new audit log entry.
    Receives log details (service, event, description, etc.) and saves them.
    """
    try:
        # Delegate log creation to the audit service
        return await audit_service.log(log_request)
    except Exception as e:
        # Return a 400 Bad Request error if logging fails
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/logs", response_model=GetLogsResponse)
async def get_logs(
    get_logs_request: GetLogsRequest = Depends(), audit_service: AuditService = Depends(get_audit_service)) -> GetLogsResponse:
    """
    Endpoint to retrieve existing audit logs.
    Supports filtering via query parameters defined in GetLogsRequest.
    """
    try:
        # Retrieve logs using the service with the provided filters
        logs = await audit_service.get_logs(get_logs_request)
        return logs
    except Exception as e:
        # Return a 400 Bad Request error if retrieval fails
        raise HTTPException(status_code=400, detail=str(e))