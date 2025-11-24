from ..repositories.i_log_repository import ILogRepository
from ..schemas.log_schema import LogRequest, LogResponse
from ..models.log_model import Log

class AuditService:
    def __init__(self, log_repository: ILogRepository):
        self.log_repository = log_repository

    async def log(self, log_request: LogRequest) -> LogResponse:
        log = Log(
            doctor_id=log_request.doctor_id,
            patient_hashed_cf=log_request.patient_hashed_cf,
            description=log_request.description,
        )

        saved_log = await self.log_repository.save(log)

        return LogResponse(
            message="Log created successfully",
            log_id=saved_log.id,
            timestamp=saved_log.created_at
        )