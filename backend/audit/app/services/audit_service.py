# Import the interface for the log repository
from ..repositories.i_log_repository import ILogRepository
# Import Pydantic schemas for request and response handling
from ..schemas.log_schema import (
    CreateLogRequest,
    CreateLogResponse,
    GetLogsResponse,
    LogItem, GetLogsRequest
)
# Import the Log domain model
from ..models.log_model import Log

class AuditService:
    """
    Service class responsible for business logic related to Audit Logging.
    Handles the creation and retrieval of audit logs.
    """
    def __init__(self, log_repository: ILogRepository):
        # Inject the log repository dependency
        self.log_repository = log_repository

    async def log(self, create_log_request: CreateLogRequest) -> CreateLogResponse:
        """
        Creates a new log entry in the system.
        Maps the request schema to the database model and saves it.
        """
        # Map fields from the request schema to the Log model
        log = Log(
            service=create_log_request.service,
            event=create_log_request.event,
            description=create_log_request.description,
            doctor_id=create_log_request.doctor_id,
            patient_hashed_cf=create_log_request.patient_hashed_cf,
            report_id=create_log_request.report_id,
            data_id=create_log_request.data_id,
        )

        # Persist the log using the repository
        saved_log = await self.log_repository.save(log)

        # Return the response containing the ID and creation timestamp
        return CreateLogResponse(
            log_id=saved_log.id,
            created_at=saved_log.created_at
        )

    async def get_logs(
        self, get_logs_request: GetLogsRequest) -> GetLogsResponse:
        """
        Retrieves logs based on the filters provided in the request.
        """
        # Fetch logs from the repository using the provided filter criteria
        logs = await self.log_repository.find_with_filters(
            service=get_logs_request.service,
            event=get_logs_request.event,
            doctor_id=get_logs_request.doctor_id,
            patient_hashed_cf=get_logs_request.patient_hashed_cf,
            report_id=get_logs_request.report_id,
            data_id=get_logs_request.data_id
        )

        # Convert the list of SQLAlchemy models to Pydantic schemas
        log_items = [LogItem.model_validate(log) for log in logs]

        # Determine the response message based on whether logs were found
        default_message = GetLogsResponse.model_fields["message"].default
        message = "No logs retrieved" if not log_items else default_message

        # Return the response object containing the list of logs
        return GetLogsResponse(
            message=message,
            logs=log_items
        )