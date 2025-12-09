import os
from typing import List, Dict, Any
from ..models.report_model import Report
from ..repositories.I_report_repository import IReportRepository
from ..services.strategies.numeric_strategy import NumericAnalysisStrategy
from ..services.strategies.image_strategy import ImageAnalysisStrategy
from ..services.strategies.text_strategy import TextAnalysisStrategy
from ..services.strategies.signal_strategy import SignalAnalysisStrategy
from ..schemas.analysis_schema import AnalysisRequest, AnalysisResponse, ReportItem, GetReportsResponse
from ..utils.http_client import HttpClient
from ..utils.logging.I_observer import IObserver

strategies = {
    "numeric": NumericAnalysisStrategy,
    "img_rx": ImageAnalysisStrategy,
    "img_skin": ImageAnalysisStrategy,
    "text": TextAnalysisStrategy,
    "signal": SignalAnalysisStrategy
}

class XAiService:
    def __init__(self, reports_repository: IReportRepository, http_client: HttpClient):
        self.reports_repository = reports_repository
        self.data_url = os.getenv("DATA_PROCESSING_URL")
        self.http = http_client
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify(self, payload: Dict[str, Any]):
        for observer in self._observers:
            await observer.update(payload)

    async def analyse(self, analysis_request: AnalysisRequest) -> AnalysisResponse:
        processed_data = await self.http.request(
            "GET",
            f"{self.data_url}/retrieve/{analysis_request.processed_data_id}",
        )

        if not processed_data:
            raise Exception(
                f"Processed data {analysis_request.processed_data_id} not found"
            )

        strategy_class = strategies.get(analysis_request.strategy)

        if not strategy_class:
            raise Exception(f"Strategy '{analysis_request.strategy}' not found")

        strategy_instance = strategy_class()

        result = await strategy_instance.analyse(processed_data)

        report = Report(
            doctor_id=analysis_request.doctor_id,
            patient_hashed_cf=analysis_request.patient_hashed_cf,
            processed_data_id=analysis_request.processed_data_id,
            strategy=analysis_request.strategy,
            diagnosis=result.get("diagnosis", "N/A"),
            confidence=result.get("confidence", 0.0),
            explanation=result.get("explanation", "N/A")
        )

        report = await self.reports_repository.save(report)

        await self.notify({
            "service": "explainable_ai",
            "event": "analysis_completed",
            "description": "Report saved in the database",
            "report_id": report.id
        })

        return AnalysisResponse(report=ReportItem.model_validate(report))

    async def get_reports(self, doctor_id: int, patient_hashed_cf: str | None = None) -> GetReportsResponse:
        reports = []

        if patient_hashed_cf:
            all_reports = await self.reports_repository.find_by_patient_hashed_cf(patient_hashed_cf)
            reports = [r for r in all_reports if r.doctor_id == doctor_id]

            await self.notify({
                "service": "explainable_ai",
                "event": "reports_patient",
                "description": "Reports view required for a patient",
                "doctor_id": doctor_id,
                "patient_hashed_cf": patient_hashed_cf
            })

        else:
            reports = await self.reports_repository.find_by_doctor_id(doctor_id)

            await self.notify({
                "service": "explainable_ai",
                "event": "reports_all",
                "description": "Reports view required",
                "doctor_id": doctor_id
            })

        reports = [ReportItem.model_validate(r) for r in reports]

        default_message = GetReportsResponse.model_fields["message"].default
        message = "No reports retrieved" if not reports else default_message

        return GetReportsResponse(message=message, reports=reports)