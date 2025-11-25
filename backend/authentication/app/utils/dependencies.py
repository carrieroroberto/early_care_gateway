import os
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.db_connection import get_session
from ..repositories.doctor_repository import DoctorRepository
from ..repositories.i_doctor_repository import IDoctorRepository
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..services.authentication_service import AuthenticationService
from ..utils.logging.audit_client import AuditClient

password_hasher = PasswordHasher()
jwt_signer = JwtSigner(secret=os.getenv("SECRET_KEY", "secret"))

audit_url = os.getenv("AUDIT_URL", "http://localhost:8000/audit")
audit_client = AuditClient(audit_url=audit_url)

async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthenticationService:
    doctor_repository: IDoctorRepository = DoctorRepository(session=session)
    auth_service = AuthenticationService(
        doctor_repository=doctor_repository,
        password_hasher=password_hasher,
        jwt_signer=jwt_signer
    )
    auth_service.attach(audit_client)
    return auth_service