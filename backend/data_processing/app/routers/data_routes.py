from fastapi import APIRouter, HTTPException, Depends, Path
from app.schemas.data_schema import DataRequest, DataResponse, GetDataResponse
from app.services.data_service import DataProcessingService
from app.utils.dependencies import get_data_service

router = APIRouter(prefix="/data_processing", tags=["Endpoints"])

@router.post("/process", response_model=DataResponse)
async def process(data_request: DataRequest, data_service: DataProcessingService = Depends(get_data_service)) -> DataResponse:
    try:
        return await data_service.process(data_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/retrieve/{data_id}", response_model=GetDataResponse)
async def retrieve(data_id: int = Path(...), data_service: DataProcessingService = Depends(get_data_service)) -> GetDataResponse:
    try:
        return await data_service.retrieve(data_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))