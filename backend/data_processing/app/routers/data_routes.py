# Import FastAPI components for routing, exception handling, and dependency injection
from fastapi import APIRouter, HTTPException, Depends, Path

# Import Pydantic schemas for data validation (request and response models)
from app.schemas.data_schema import DataRequest, DataResponse, GetDataResponse

# Import the DataProcessingService class to handle business logic
from app.services.data_service import DataProcessingService

# Import the dependency function to retrieve the service instance
from app.utils.dependencies import get_data_service

# Initialize the API router with a specific prefix and tags for documentation
router = APIRouter(prefix="/data_processing", tags=["Endpoints"])

@router.post("/process", response_model=DataResponse)
async def process(data_request: DataRequest, data_service: DataProcessingService = Depends(get_data_service)) -> DataResponse:
    """
    Endpoint to process raw data.
    Receives data validation strategy and raw data, then delegates processing to the service.
    """
    try:
        # Call the process method of the data service with the request body
        return await data_service.process(data_request)
    except Exception as e:
        # Catch any errors during processing and return a 400 Bad Request response
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/retrieve/{data_id}", response_model=GetDataResponse)
async def retrieve(data_id: int = Path(...), data_service: DataProcessingService = Depends(get_data_service)) -> GetDataResponse:
    """
    Endpoint to retrieve processed data by its ID.
    The data_id is extracted from the URL path.
    """
    try:
        # Call the retrieve method of the data service using the provided ID
        return await data_service.retrieve(data_id)
    except Exception as e:
        # Catch any errors (e.g., data not found) and return a 400 Bad Request response
        raise HTTPException(status_code=400, detail=str(e))