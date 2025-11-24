from pydantic import BaseModel, Field
from datetime import datetime

class LogRequest(BaseModel):
    doctor_id: int = Field(..., ge=1)
    patient_hashed_cf: str | None = Field(None, min_length=2)
    description: str = Field(..., min_length=1)

class LogResponse(BaseModel):
    message: str = "Log created successfully"
    log_id: int
    timestamp: datetime