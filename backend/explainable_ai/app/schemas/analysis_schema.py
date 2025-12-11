from typing import List
# Import Pydantic components for data validation
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class AnalysisRequest(BaseModel):
    """
    Schema for the incoming analysis request.
    """
    doctor_id: int
    patient_hashed_cf: str
    # The type of analysis to perform (e.g., 'numeric', 'text')
    strategy: str
    # ID of the data that has already been processed by the Data Processing service
    processed_data_id: int

class ReportItem(BaseModel):
    """
    Schema representing a detailed analysis report.
    Used for response serialization.
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

    # Configuration to allow creating instances from ORM objects
    model_config = ConfigDict(from_attributes=True)

class AnalysisResponse(BaseModel):
    """
    Response returned after a successful analysis.
    """
    message: str = "Report saved into the database successfully"
    report: ReportItem

class GetReportsResponse(BaseModel):
    """
    Response returned when retrieving a list of reports.
    """
    message: str = "Report(s) retrieved successfully"
    reports: List[ReportItem]