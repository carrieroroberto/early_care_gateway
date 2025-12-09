from pydantic import BaseModel
from datetime import datetime
from typing import List

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

class AnalyseRequest(BaseModel):
    patient_hashed_cf: str
    strategy: str
    raw_data: str

class AnalyseResponse(BaseModel):
    message: str
    report: ReportItem

class GetReportsResponse(BaseModel):
    message: str
    reports: List[ReportItem]