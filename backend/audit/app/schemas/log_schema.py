from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CreateLogRequest(BaseModel):
    service: str = Field(..., min_length=1, max_length=50)
    event: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=100)
    doctor_id: int | None = Field(None, ge=1)
    patient_hashed_cf: str | None = Field(None, min_length=1, max_length=255)
    report_id: int | None = Field(None)
    data_id: int | None = Field(None)

class CreateLogResponse(BaseModel):
    message: str = Field("Log created successfully")
    log_id: int = Field(...)
    created_at: datetime = Field(...)

class GetLogsRequest(BaseModel):
    service: str | None = None
    event: str | None = None
    doctor_id: int | None = Field(None, ge=1)
    patient_hashed_cf: str | None = None
    report_id: int | None = Field(None, ge=1)
    data_id: int | None = Field(None, ge=1)

class LogItem(BaseModel):
    id: int
    service: str
    event: str
    description: str
    doctor_id: int | None
    patient_hashed_cf: str | None
    report_id: int | None
    data_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class GetLogsResponse(BaseModel):
    message: str = Field("Log(s) retrieved successfully")
    logs: List[LogItem] = Field(default_factory=list)