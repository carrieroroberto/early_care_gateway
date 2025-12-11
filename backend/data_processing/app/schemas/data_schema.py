# Import Pydantic components for data validation and serialization
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class DataRequest(BaseModel):
    """
    Schema for the incoming data processing request.
    """
    # The processing strategy to apply (e.g., 'numeric', 'text')
    strategy: str = Field(...)
    # The raw data to be processed (e.g., JSON string or Base64 encoded string)
    raw_data: str = Field(...)

class ProcessedDataItem(BaseModel):
    """
    Schema representing a single processed data item.
    Used for retrieving data.
    """
    id: int
    type: str
    data: str
    created_at: datetime

    # Configuration to allow creation from ORM attributes
    model_config = ConfigDict(from_attributes=True)

class DataResponse(BaseModel):
    """
    Schema for the response after successful processing.
    """
    message: str = "Processed data saved into the database successfully"
    processed_data_id: int

class GetDataResponse(BaseModel):
    """
    Schema for the response when retrieving processed data.
    """
    message: str = "Processed data retrieved successfully"
    data: ProcessedDataItem