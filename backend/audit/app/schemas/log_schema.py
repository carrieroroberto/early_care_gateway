from typing import List
# Import Pydantic components for validation
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CreateLogRequest(BaseModel):
    """
    Schema for the request to create a new log entry.
    """
    service: str = Field(..., min_length=1, max_length=50)
    event: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=100)
    # Optional fields to link context to the log
    doctor_id: int | None = Field(None, ge=1)
    patient_hashed_cf: str | None = Field(None, min_length=1, max_length=255)
    report_id: int | None = Field(None)
    data_id: int | None = Field(None)

class CreateLogResponse(BaseModel):
    """
    Schema for the response after a log is successfully created.
    """
    message: str = Field("Log created successfully")
    log_id: int = Field(...)
    created_at: datetime = Field(...)

class GetLogsRequest(BaseModel):
    """
    Schema defining the query filters for retrieving logs.
    """
    service: str | None = None
    event: str | None = None
    doctor_id: int | None = Field(None, ge=1)
    patient_hashed_cf: str | None = None
    report_id: int | None = Field(None, ge=1)
    data_id: int | None = Field(None, ge=1)

class LogItem(BaseModel):
    """
    Schema representing a single log entry in the response list.
    """
    id: int
    service: str
    event: str
    description: str
    doctor_id: int | None
    patient_hashed_cf: str | None
    report_id: int | None
    data_id: int | None
    created_at: datetime

    # Enable ORM mode to allow creating schema instances from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)

class GetLogsResponse(BaseModel):
    """
    Schema for the response containing a list of retrieved logs.
    """
    message: str = Field("Log(s) retrieved successfully")
    logs: List[LogItem] = Field(default_factory=list)