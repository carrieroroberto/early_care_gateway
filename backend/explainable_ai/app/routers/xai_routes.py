from fastapi import APIRouter, HTTPException, Depends, Path, Query
from app.schemas.analysis_schema import AnalysisRequest, AnalysisResponse, GetReportsResponse
from app.services.xai_service import XAiService
from app.utils.dependencies import get_xai_service

router = APIRouter(prefix="/explainable_ai", tags=["Endpoints"])

@router.post("/analyse", response_model=AnalysisResponse)
async def analyse(analysis_request: AnalysisRequest, xai_service: XAiService = Depends(get_xai_service)) -> AnalysisResponse:
    try:
        return await xai_service.analyse(analysis_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reports/{doctor_id}", response_model=GetReportsResponse)
async def get_reports(doctor_id: int = Path(...), patient_hashed_cf: str | None = Query(None), xai_service: XAiService = Depends(get_xai_service)) -> GetReportsResponse:
    try:
        return await xai_service.get_reports(doctor_id=doctor_id, patient_hashed_cf=patient_hashed_cf)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))