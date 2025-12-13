from typing import List, Dict, Any
# Import the Observer interface for the audit system
from ..utils.logging.I_observer import IObserver
# Import the interface for the doctor repository
from ..repositories.i_doctor_repository import IDoctorRepository
# Import schemas for request/response handling
from ..schemas.doctor_schema import RegisterDoctorRequest, LoginDoctorRequest, RegisterDoctorResponse, \
    LoginDoctorResponse, ValidateTokenResponse, ValidateTokenRequest
# Import utility classes for password hashing and JWT signing
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
# Import the Doctor domain model
from ..models.doctor_model import Doctor


class AuthenticationService:
    """
    Service class handling the business logic for doctor authentication.
    It implements the Subject part of the Observer pattern to notify listeners (e.g., Audit service) about events.
    """

    def __init__(
            self, doctor_repository: IDoctorRepository, password_hasher: PasswordHasher, jwt_signer: JwtSigner
    ):
        # Inject dependencies: repository for database access, hasher for security, and jwt signer for tokens
        self.doctorRepository = doctor_repository
        self.passwordHasher = password_hasher
        self.jwtSigner = jwt_signer
        # List to hold attached observers
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver):
        """
        Attaches an observer to the service.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver):
        """
        Detaches an observer from the service.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify(self, payload: Dict[str, Any]):
        """
        Notifies all attached observers with a specific payload (e.g., event details).
        """
        for observer in self._observers:
            await observer.update(payload)

    async def register_doctor(self, register_doctor_request: RegisterDoctorRequest) -> RegisterDoctorResponse:
        """
        Registers a new doctor in the system.
        """
        # Check if a doctor with the given email already exists
        existing_doctor = await self.doctorRepository.find_by_email(str(register_doctor_request.email))
        if existing_doctor:
            # Notify observers about the registration failure
            await self.notify({
                "service": "authentication",
                "event": "register_fail",
                "description": f"Email already registered: {register_doctor_request.email}"
            })
            raise Exception("Email already registered")

        # Hash the password before storing it
        hashed_pwd = self.passwordHasher.hash(register_doctor_request.password)

        # Create a new Doctor model instance
        doctor = Doctor(
            name=register_doctor_request.name,
            surname=register_doctor_request.surname,
            email=str(register_doctor_request.email),
            hashed_password=hashed_pwd
        )
        # Save the doctor to the database via the repository
        saved_doctor = await self.doctorRepository.save(doctor)

        # Notify observers about the successful registration
        await self.notify({
            "service": "authentication",
            "event": "register_success",
            "description": "Doctor registered successfully",
            "doctor_id": saved_doctor.id
        })

        # Return the response with the new doctor's ID
        return RegisterDoctorResponse(doctor_id=saved_doctor.id)

    async def login_doctor(self, login_request: LoginDoctorRequest) -> LoginDoctorResponse:
        """
        Authenticates a doctor and issues a JWT token with doctor_id, name, and surname.
        """
        # Retrieve the doctor by email
        doctor = await self.doctorRepository.find_by_email(str(login_request.email))

        if not doctor or not self.passwordHasher.verify(login_request.password, doctor.hashed_password):
            await self.notify({
                "service": "authentication",
                "event": "login_fail",
                "description": "Invalid credentials",
            })
            raise Exception("Invalid credentials")

        # Create a JWT token including doctor_id, name, and surname
        token = self.jwtSigner.create_token(
            doctor_id=str(doctor.id),
            name=doctor.name,
            surname=doctor.surname
        )

        await self.notify({
            "service": "authentication",
            "event": "login_success",
            "description": "Doctor logged in successfully",
            "doctor_id": doctor.id
        })

        return LoginDoctorResponse(jwt_token=token)

    async def validate_token(self, token_request: ValidateTokenRequest) -> ValidateTokenResponse:
        """
        Validates the provided JWT token.
        """
        try:
            # Verify the token signature and expiration
            payload = self.jwtSigner.verify_token(token_request.token)

            # Extract the subject (doctor_id) from the token payload
            doctor_id = payload.get("sub")
            if not doctor_id:
                await self.notify({
                    "service": "authentication",
                    "event": "validate_token_fail",
                    "description": "Invalid token: missing doctor_id"
                })
                raise Exception("Invalid token: missing doctor_id")

            # Verify that the doctor associated with the token actually exists
            doctor = await self.doctorRepository.find_by_id(int(doctor_id))
            if not doctor:
                await self.notify({
                    "service": "authentication",
                    "event": "validate_token_fail",
                    "description": "Doctor not found"
                })
                raise Exception("Doctor not found")

            # Notify observers about the successful token validation
            await self.notify({
                "service": "authentication",
                "event": "validate_token_success",
                "description": "Token successfully validated",
                "doctor_id": doctor.id
            })

            # Return the response confirming the doctor ID
            return ValidateTokenResponse(doctor_id=doctor.id)

        except Exception as e:
            # Handle any exceptions during validation (e.g., expired token, bad signature)
            await self.notify({
                "service": "authentication",
                "event": "validate_token_fail",
                "description": "Invalid or expired token",
            })
            raise Exception(f"Invalid or expired token: {str(e)}")