from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class DataRequest(BaseModel):
    strategy: str = Field(...)
    raw_data: str = Field(...)

class ProcessedDataItem(BaseModel):
    id: int
    type: str
    data: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DataResponse(BaseModel):
    message: str = "Processed data saved into the database successfully"
    processed_data_id: int

class GetDataResponse(BaseModel):
    message: str = "Processed data retrieved successfully"
    data: ProcessedDataItem
