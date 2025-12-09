from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class AnalysisRequest(BaseModel):
    doctor_id: int
    patient_hashed_cf: str
    strategy: str
    processed_data_id: int

class ReportItem(BaseModel):
    id: int
    doctor_id: int
    patient_hashed_cf: str
    processed_data_id: int
    created_at: datetime
    strategy: str
    diagnosis: str
    confidence: float
    explanation: str

    model_config = ConfigDict(from_attributes=True)

class AnalysisResponse(BaseModel):
    message: str = "Report saved into the database successfully"
    report: ReportItem

class GetReportsResponse(BaseModel):
    message: str = "Report(s) retrieved successfully"
    reports: List[ReportItem]