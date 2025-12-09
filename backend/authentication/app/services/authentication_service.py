from typing import List, Dict, Any
from ..utils.logging.I_observer import IObserver
from ..repositories.i_doctor_repository import IDoctorRepository
from ..schemas.doctor_schema import RegisterDoctorRequest, LoginDoctorRequest, RegisterDoctorResponse, \
    LoginDoctorResponse, ValidateTokenResponse, ValidateTokenRequest
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..models.doctor_model import Doctor

class AuthenticationService:
    def __init__(
        self, doctor_repository: IDoctorRepository, password_hasher: PasswordHasher, jwt_signer: JwtSigner
    ):
        self.doctorRepository = doctor_repository
        self.passwordHasher = password_hasher
        self.jwtSigner = jwt_signer
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify(self, payload: Dict[str, Any]):
        for observer in self._observers:
            await observer.update(payload)

    async def register_doctor(self, register_doctor_request: RegisterDoctorRequest) -> RegisterDoctorResponse:
        existing_doctor = await self.doctorRepository.find_by_email(str(register_doctor_request.email))
        if existing_doctor:
            await self.notify({
                "service": "authentication",
                "event": "register_fail",
                "description": f"Email already registered: {register_doctor_request.email}"
            })
            raise Exception("Email already registered")

        hashed_pwd = self.passwordHasher.hash(register_doctor_request.password)
        doctor = Doctor(
            name=register_doctor_request.name,
            surname=register_doctor_request.surname,
            email=str(register_doctor_request.email),
            hashed_password=hashed_pwd
        )
        saved_doctor = await self.doctorRepository.save(doctor)

        await self.notify({
            "service": "authentication",
            "event": "register_success",
            "description": "Doctor registered successfully",
            "doctor_id": saved_doctor.id
        })

        return RegisterDoctorResponse(doctor_id=saved_doctor.id)

    async def login_doctor(self, login_request: LoginDoctorRequest) -> LoginDoctorResponse:
        doctor = await self.doctorRepository.find_by_email(str(login_request.email))
        if not doctor or not self.passwordHasher.verify(login_request.password, doctor.hashed_password):
            await self.notify({
                "service": "authentication",
                "event": "login_fail",
                "description": "Invalid credentials",
            })
            raise Exception("Invalid credentials")

        token = self.jwtSigner.create_token(str(doctor.id))

        await self.notify({
            "service": "authentication",
            "event": "login_success",
            "description": "Doctor logged in successfully",
            "doctor_id": doctor.id
        })

        return LoginDoctorResponse(jwt_token=token)

    async def validate_token(self, token_request: ValidateTokenRequest) -> ValidateTokenResponse:
        try:
            payload = self.jwtSigner.verify_token(token_request.token)
            doctor_id = payload.get("sub")
            if not doctor_id:
                await self.notify({
                    "service": "authentication",
                    "event": "validate_token_fail",
                    "description": "Invalid token: missing doctor_id"
                })
                raise Exception("Invalid token: missing doctor_id")

            doctor = await self.doctorRepository.find_by_id(int(doctor_id))
            if not doctor:
                await self.notify({
                    "service": "authentication",
                    "event": "validate_token_fail",
                    "description": "Doctor not found"
                })
                raise Exception("Doctor not found")

            await self.notify({
                "service": "authentication",
                "event": "validate_token_success",
                "description": "Token successfully validated",
                "doctor_id": doctor.id
            })

            return ValidateTokenResponse(doctor_id=doctor.id)

        except Exception as e:
            await self.notify({
                "service": "authentication",
                "event": "validate_token_fail",
                "description": "Invalid or expired token",
            })
            raise Exception(f"Invalid or expired token: {str(e)}")