from ..repositories.i_doctor_repository import IDoctorRepository
from ..schemas.doctor_schema import RegisterDoctorRequest, LoginDoctorRequest, RegisterDoctorResponse, \
    LoginDoctorResponse, ValidateTokenResponse, ValidateTokenRequest
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..models.doctor_model import Doctor

class AuthenticationService:
    def __init__(
        self, doctor_repository: IDoctorRepository, password_hasher: PasswordHasher, jwt_signer: JwtSigner):
        self.doctorRepository = doctor_repository
        self.passwordHasher = password_hasher
        self.jwtSigner = jwt_signer

    async def register_doctor(self, register_doctor_request: RegisterDoctorRequest) -> RegisterDoctorResponse:
        existing_doctor = await self.doctorRepository.find_by_email(str(register_doctor_request.email))
        if existing_doctor:
            raise Exception("Email already registered")

        hashed_pwd = self.passwordHasher.hash(register_doctor_request.password)
        doctor = Doctor(
            name=register_doctor_request.name,
            surname=register_doctor_request.surname,
            email=str(register_doctor_request.email),
            hashed_password=hashed_pwd
        )
        saved_doctor = await self.doctorRepository.save(doctor)
        return RegisterDoctorResponse(doctor_id=saved_doctor.id)

    async def login_doctor(self, login_request: LoginDoctorRequest) -> LoginDoctorResponse:
        doctor = await self.doctorRepository.find_by_email(str(login_request.email))
        if not doctor or not self.passwordHasher.verify(login_request.password, doctor.hashed_password):
            raise Exception("Invalid credentials")

        token = self.jwtSigner.create_token(str(doctor.id))
        return LoginDoctorResponse(jwt_token=token)

    async def validate_token(self, token_request: ValidateTokenRequest) -> ValidateTokenResponse:
        try:
            payload = self.jwtSigner.verify_token(token_request.token)
            doctor_id = payload.get("sub")

            if not doctor_id:
                raise Exception("Invalid token: missing doctor_id")

            doctor = await self.doctorRepository.find_by_id(int(doctor_id))
            if not doctor:
                raise Exception("Doctor not found")

            return ValidateTokenResponse(doctor_id=doctor.id)

        except Exception as e:
            raise Exception(f"Invalid or expired token: {str(e)}")