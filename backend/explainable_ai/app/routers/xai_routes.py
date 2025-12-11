# Import FastAPI components for routing, exception handling, and dependency injection
from fastapi import APIRouter, HTTPException, Depends, Path, Query
# Import Pydantic schemas for request and response validation
from app.schemas.analysis_schema import AnalysisRequest, AnalysisResponse, GetReportsResponse
# Import the XAI service class to handle business logic
from app.services.xai_service import XAiService
# Import the dependency function to retrieve the service instance
from app.utils.dependencies import get_xai_service

# Initialize the API router with a specific prefix and tags for documentation
router = APIRouter(prefix="/explainable_ai", tags=["Endpoints"])

@router.post("/analyse", response_model=AnalysisResponse)
async def analyse(analysis_request: AnalysisRequest, xai_service: XAiService = Depends(get_xai_service)) -> AnalysisResponse:
    """
    Endpoint to trigger an Explainable AI analysis.
    Receives analysis parameters and delegates the task to the XAI service.
    """
    try:
        # Call the analyse method of the XAI service
        return await xai_service.analyse(analysis_request)
    except Exception as e:
        # Catch any errors during analysis and return a 400 Bad Request response
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reports/{doctor_id}", response_model=GetReportsResponse)
async def get_reports(doctor_id: int = Path(...), patient_hashed_cf: str | None = Query(None), xai_service: XAiService = Depends(get_xai_service)) -> GetReportsResponse:
    """
    Endpoint to retrieve analysis reports for a specific doctor.
    Supports optional filtering by patient's hashed fiscal code (CF).
    """
    try:
        # Call the get_reports method of the XAI service
        return await xai_service.get_reports(doctor_id=doctor_id, patient_hashed_cf=patient_hashed_cf)
    except Exception as e:
        # Catch any errors and return a 400 Bad Request response
        raise HTTPException(status_code=400, detail=str(e))