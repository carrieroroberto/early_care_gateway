from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .db_connection import get_session
from ..repositories.doctor_repository import DoctorRepository
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..services.authentication_service import AuthenticationService
import os

password_hasher = PasswordHasher()
jwt_signer = JwtSigner(secret=os.getenv("SECRET_KEY", "secret"))

async def get_auth_service(session: AsyncSession = Depends(get_session)):
    doctor_repository = DoctorRepository(session=session)

    return AuthenticationService(
        doctorRepository=doctor_repository,
        passwordHasher=password_hasher,
        jwtSigner=jwt_signer
    )