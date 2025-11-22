from ..repositories.doctor_repository import DoctorRepository
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..models.doctor_model import Doctor

class AuthenticationService:
    def __init__(
        self,
        doctorRepository: DoctorRepository,
        passwordHasher: PasswordHasher,
        jwtSigner: JwtSigner
    ):
        self.doctorRepository = doctorRepository
        self.passwordHasher = passwordHasher
        self.jwtSigner = jwtSigner

    async def registerDoctor(self, name: str, surname: str, email: str, password: str):
        existing_doctor = await self.doctorRepository.find_by_email(email)
        if existing_doctor:
            raise Exception("Email already registered")

        hashed_pw = self.passwordHasher.hash(password)
        doctor = Doctor(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_pw
        )

        return await self.doctorRepository.save(doctor)

    async def loginDoctor(self, email: str, password: str):
        doctor = await self.doctorRepository.find_by_email(email)

        if not doctor or not self.passwordHasher.verify(password, doctor.hashed_password):
            raise Exception("Invalid credentials")

        return self.jwtSigner.create_token(str(doctor.id))

    async def validateToken(self, token: str):
        try:
            payload = self.jwtSigner.verify_token(token)
            doctor_id = payload.get("sub")

            if not doctor_id:
                raise Exception("Invalid token: missing doctor_id (sub)")

            doctor = await self.doctorRepository.find_by_id(int(doctor_id))
            if not doctor:
                raise Exception("Doctor not found")

            return doctor.id

        except Exception as e:
            raise Exception(f"Invalid or expired token: {str(e)}")