import os
from typing import List, Dict, Any
# Import domain models, repositories, and specific strategies
from ..models.report_model import Report
from ..repositories.I_report_repository import IReportRepository
from ..services.strategies.numeric_strategy import NumericAnalysisStrategy
from ..services.strategies.image_strategy import ImageAnalysisStrategy
from ..services.strategies.text_strategy import TextAnalysisStrategy
from ..services.strategies.signal_strategy import SignalAnalysisStrategy
# Import schemas for request/response handling
from ..schemas.analysis_schema import AnalysisRequest, AnalysisResponse, ReportItem, GetReportsResponse
# Import utilities for HTTP requests and Observer pattern
from ..utils.http_client import HttpClient
from ..utils.logging.I_observer import IObserver

# Registry mapping strategy names to their concrete class implementations
strategies = {
    "numeric": NumericAnalysisStrategy,
    "img_rx": ImageAnalysisStrategy,
    "img_skin": ImageAnalysisStrategy,
    "text": TextAnalysisStrategy,
    "signal": SignalAnalysisStrategy
}

class XAiService:
    """
    Main service orchestrating the Explainable AI workflow.
    It fetches processed data, selects the appropriate AI strategy,
    saves the results, and notifies observers (Audit).
    """
    def __init__(self, reports_repository: IReportRepository, http_client: HttpClient):
        # Inject repository and HTTP client dependencies
        self.reports_repository = reports_repository
        # URL for the Data Processing service to fetch prepared data
        self.data_url = os.getenv("DATA_PROCESSING_URL")
        self.http = http_client
        # List of observers for the Observer pattern
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver):
        """
        Attaches an observer to listen for service events.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver):
        """
        Detaches an observer from the service.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify(self, payload: Dict[str, Any]):
        """
        Notifies all observers of a specific event.
        """
        for observer in self._observers:
            await observer.update(payload)

    async def analyse(self, analysis_request: AnalysisRequest) -> AnalysisResponse:
        """
        Performs the full analysis workflow:
        1. Retrieve processed data from Data Processing service.
        2. Select the correct AI strategy.
        3. Run inference.
        4. Save the report.
        """
        # Step 1: Fetch the pre-processed data using the ID provided in the request
        processed_data = await self.http.request(
            "GET",
            f"{self.data_url}/retrieve/{analysis_request.processed_data_id}",
        )

        if not processed_data:
            raise Exception(
                f"Processed data {analysis_request.processed_data_id} not found"
            )

        # Step 2: Select the strategy class based on the requested strategy type
        strategy_class = strategies.get(analysis_request.strategy)

        if not strategy_class:
            raise Exception(f"Strategy '{analysis_request.strategy}' not found")

        # Instantiate the selected strategy
        strategy_instance = strategy_class()

        # Step 3: Execute the analysis using the strategy
        result = await strategy_instance.analyse(processed_data)

        # Create a Report model to persist the results
        report = Report(
            doctor_id=analysis_request.doctor_id,
            patient_hashed_cf=analysis_request.patient_hashed_cf,
            processed_data_id=analysis_request.processed_data_id,
            strategy=analysis_request.strategy,
            diagnosis=result.get("diagnosis", "N/A"),
            confidence=result.get("confidence", 0.0),
            explanation=result.get("explanation", "N/A")
        )

        # Step 4: Save the report to the database
        report = await self.reports_repository.save(report)

        # Notify observers (Audit) about the completed analysis
        await self.notify({
            "service": "explainable_ai",
            "event": "analysis_completed",
            "description": "Report saved in the database",
            "report_id": report.id
        })

        return AnalysisResponse(report=ReportItem.model_validate(report))

    async def get_reports(self, doctor_id: int, patient_hashed_cf: str | None = None) -> GetReportsResponse:
        """
        Retrieves analysis reports.
        Can filter by doctor ID and optionally by patient hash.
        """
        reports = []

        if patient_hashed_cf:
            # Fetch reports for a specific patient under a specific doctor
            all_reports = await self.reports_repository.find_by_patient_hashed_cf(patient_hashed_cf)
            reports = [r for r in all_reports if r.doctor_id == doctor_id]

            # Audit log for accessing patient specific data
            await self.notify({
                "service": "explainable_ai",
                "event": "reports_patient",
                "description": "Reports view required for a patient",
                "doctor_id": doctor_id,
                "patient_hashed_cf": patient_hashed_cf
            })

        else:
            # Fetch all reports for the doctor
            reports = await self.reports_repository.find_by_doctor_id(doctor_id)

            # Audit log for accessing general reports
            await self.notify({
                "service": "explainable_ai",
                "event": "reports_all",
                "description": "Reports view required",
                "doctor_id": doctor_id
            })

        # Convert ORM models to Pydantic schemas
        reports = [ReportItem.model_validate(r) for r in reports]

        # Determine the response message
        default_message = GetReportsResponse.model_fields["message"].default
        message = "No reports retrieved" if not reports else default_message

        return GetReportsResponse(message=message, reports=reports)