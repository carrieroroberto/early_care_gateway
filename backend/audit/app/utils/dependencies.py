from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .db_connection import get_session
from ..repositories.doctor_repository import DoctorRepository
from ..repositories.i_doctor_repository import IDoctorRepository
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..services.authentication_service import AuthenticationService
import os

password_hasher = PasswordHasher()
jwt_signer = JwtSigner(secret=os.getenv("SECRET_KEY", "secret"))

async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthenticationService:
    doctor_repository: IDoctorRepository = DoctorRepository(session=session)

    return AuthenticationService(
        doctor_repository=doctor_repository,
        password_hasher=password_hasher,
        jwt_signer=jwt_signer
    )