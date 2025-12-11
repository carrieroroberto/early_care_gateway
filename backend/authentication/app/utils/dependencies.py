import os
# Import FastAPI dependency injection marker
from fastapi import Depends
# Import AsyncSession type for type hinting
from sqlalchemy.ext.asyncio import AsyncSession
# Import internal utilities and services
from ..utils.db_connection import get_session
from ..repositories.doctor_repository import DoctorRepository
from ..repositories.i_doctor_repository import IDoctorRepository
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..services.authentication_service import AuthenticationService
from ..utils.logging.audit_client import AuditClient
from ..utils.http_client import HttpClient

# Initialize shared utility instances
password_hasher = PasswordHasher()
# Initialize JWT signer with the secret key from environment variables
jwt_signer = JwtSigner(secret=os.getenv("SECRET_KEY", "secret"))

# Configure the Audit service URL and client
audit_url = os.getenv("AUDIT_URL", "http://audit_service:8000/audit")
http_client = HttpClient()
audit_client = AuditClient(audit_url=audit_url, http_client=http_client)


async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthenticationService:
    """
    Dependency to construct and provide the AuthenticationService.
    Injects the database repository, password hasher, and JWT signer.
    Also attaches the AuditClient as an observer for logging events.
    """
    # Create the concrete repository implementation using the current DB session
    doctor_repository: IDoctorRepository = DoctorRepository(session=session)

    # Instantiate the service with all required dependencies
    auth_service = AuthenticationService(
        doctor_repository=doctor_repository,
        password_hasher=password_hasher,
        jwt_signer=jwt_signer
    )

    # Attach the audit client to listen for authentication events (Observer pattern)
    auth_service.attach(audit_client)

    return auth_service