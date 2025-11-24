from ..repositories.i_log_repository import ILogRepository
from ..schemas.log_schema import CreateLogRequest, CreateLogResponse, GetLogsByDoctorResponse, LogItem
from ..models.log_model import Log

class AuditService:
    def __init__(self, log_repository: ILogRepository):
        self.log_repository = log_repository

    async def log(self, create_log_request: CreateLogRequest) -> CreateLogResponse:
        log = Log(
            service=create_log_request.service,
            event=create_log_request.event,
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

    async def get_logs_by_doctor(self, doctor_id: int) -> GetLogsByDoctorResponse:
        logs = await self.log_repository.find_by_doctor_id(doctor_id)

        log_items = [
            LogItem(
                id=log.id,
                service=log.service,
                event=log.event,
                patient_hashed_cf=log.patient_hashed_cf,
                report_id=log.report_id,
                data_id=log.data_id,
                created_at=log.created_at
            )
            for log in logs or []
        ]

        default_message = GetLogsByDoctorResponse.model_fields['message'].default
        message = "No logs retrieved" if not log_items else default_message

        return GetLogsByDoctorResponse(
            message=message,
            doctor_id=doctor_id,
            logs=log_items
        )