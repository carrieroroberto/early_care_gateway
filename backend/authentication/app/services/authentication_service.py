from ..repositories.doctor_repository import DoctorRepository
from ..schemas.doctor_schema import RegisterDoctorRequest, LoginDoctorRequest, RegisterDoctorResponse, \
    LoginDoctorResponse, ValidateTokenResponse, ValidateTokenRequest
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..models.doctor_model import Doctor

class AuthenticationService:
    def __init__(self, doctorRepository: DoctorRepository, passwordHasher: PasswordHasher, jwtSigner: JwtSigner):
        self.doctorRepository = doctorRepository
        self.passwordHasher = passwordHasher
        self.jwtSigner = jwtSigner

    async def registerDoctor(self, registerDoctorRequest: RegisterDoctorRequest) -> RegisterDoctorResponse:
        existing_doctor = await self.doctorRepository.find_by_email(str(registerDoctorRequest.email))
        if existing_doctor:
            raise Exception("Email already registered")

        hashed_pw = self.passwordHasher.hash(registerDoctorRequest.password)
        doctor = Doctor(
            name=registerDoctorRequest.name,
            surname=registerDoctorRequest.surname,
            email=str(registerDoctorRequest.email),
            hashed_password=hashed_pw
        )
        saved_doctor = await self.doctorRepository.save(doctor)
        return RegisterDoctorResponse(doctor_id=saved_doctor.id)

    async def loginDoctor(self, loginRequest: LoginDoctorRequest) -> LoginDoctorResponse:
        doctor = await self.doctorRepository.find_by_email(str(loginRequest.email))
        if not doctor or not self.passwordHasher.verify(loginRequest.password, doctor.hashed_password):
            raise Exception("Invalid credentials")

        token = self.jwtSigner.create_token(str(doctor.id))
        return LoginDoctorResponse(jwt_token=token)

    async def validateToken(self, tokenRequest: ValidateTokenRequest) -> ValidateTokenResponse:
        try:
            payload = self.jwtSigner.verify_token(tokenRequest.token)
            doctor_id = payload.get("sub")

            if not doctor_id:
                raise Exception("Invalid token: missing doctor_id")

            doctor = await self.doctorRepository.find_by_id(int(doctor_id))
            if not doctor:
                raise Exception("Doctor not found")

            return ValidateTokenResponse(doctor_id=doctor.id)

        except Exception as e:
            raise Exception(f"Invalid or expired token: {str(e)}")