# Import Pydantic models and standard types
from pydantic import BaseModel
from datetime import datetime
from typing import List

class ReportItem(BaseModel):
    """
    Schema representing a detailed report item from the XAI analysis.
    """
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
    """
    Schema for the request body to initiate an analysis.
    """
    patient_hashed_cf: str
    strategy: str
    raw_data: str

class AnalyseResponse(BaseModel):
    """
    Schema for the response after initiating an analysis.
    Returns a message and the generated report item.
    """
    message: str
    report: ReportItem

class GetReportsResponse(BaseModel):
    """
    Schema for the response when retrieving a list of reports.
    """
    message: str
    # List of ReportItem objects
    reports: List[ReportItem]