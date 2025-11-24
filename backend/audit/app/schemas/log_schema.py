from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

class CreateLogRequest(BaseModel):
    service: str = Field(..., min_length=1, max_length=50)
    event: str = Field(..., min_length=1, max_length=50)
    doctor_id: int | None = Field(None, ge=1)
    patient_hashed_cf: str | None = Field(None, min_length=1, max_length=255)
    report_id: int | None = Field(None)
    data_id: int | None = Field(None)

class CreateLogResponse(BaseModel):
    message: str = Field("Log created successfully")
    log_id: int = Field(...)
    created_at: datetime = Field(...)

class LogItem(BaseModel):
    id: int
    service: str
    event: str
    patient_hashed_cf: str | None
    report_id: int | None
    data_id: int | None
    created_at: datetime

class GetLogsByDoctorResponse(BaseModel):
    message: str = Field("Log(s) retrieved successfully")
    doctor_id: int
    logs: List[LogItem] = Field(default_factory=list)