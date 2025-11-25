from ..repositories.i_log_repository import ILogRepository
from ..schemas.log_schema import (
    CreateLogRequest,
    CreateLogResponse,
    GetLogsResponse,
    LogItem, GetLogsRequest
)
from ..models.log_model import Log

class AuditService:
    def __init__(self, log_repository: ILogRepository):
        self.log_repository = log_repository

    async def log(self, create_log_request: CreateLogRequest) -> CreateLogResponse:
        log = Log(
            service=create_log_request.service,
            event=create_log_request.event,
            description=create_log_request.description,
            doctor_id=create_log_request.doctor_id,
            patient_hashed_cf=create_log_request.patient_hashed_cf,
            report_id=create_log_request.report_id,
            data_id=create_log_request.data_id,
        )

        saved_log = await self.log_repository.save(log)

        return CreateLogResponse(
            log_id=saved_log.id,
            created_at=saved_log.created_at
        )

    async def get_logs(
        self, get_logs_request: GetLogsRequest) -> GetLogsResponse:

        logs = await self.log_repository.find_with_filters(
            service=get_logs_request.service,
            event=get_logs_request.event,
            doctor_id=get_logs_request.doctor_id,
            patient_hashed_cf=get_logs_request.patient_hashed_cf,
            report_id=get_logs_request.report_id,
            data_id=get_logs_request.data_id
        )

        log_items = [
            LogItem(
                id=log.id,
                service=log.service,
                event=log.event,
                description=log.description,
                doctor_id=log.doctor_id,
                patient_hashed_cf=log.patient_hashed_cf,
                report_id=log.report_id,
                data_id=log.data_id,
                created_at=log.created_at
            )
            for log in logs
        ]

        default_message = GetLogsResponse.model_fields["message"].default
        message = "No logs retrieved" if not log_items else default_message

        return GetLogsResponse(
            message=message,
            logs=log_items
        )