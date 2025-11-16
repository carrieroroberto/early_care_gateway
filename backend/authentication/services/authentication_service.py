from ..repositories.user_repository import IUserRepository
from ..utils.audit_notifier import IAuditNotifier
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..models.user_model import User

class AuthenticationService:
    def __init__(
        self,
        userRepository: IUserRepository,
        auditNotifier: IAuditNotifier,
        passwordHasher: PasswordHasher,
        jwtSigner: JwtSigner
    ):
        self.userRepository = userRepository
        self.auditNotifier = auditNotifier
        self.passwordHasher = passwordHasher
        self.jwtSigner = jwtSigner

    def registerUser(self, email: str, password: str):
        existing = self.userRepository.findByEmail(email)
        if existing:
            raise ValueError("Email already registered")

        hashed = self.passwordHasher.hash(password)
        user = User(id=1, email=email, password_hash=hashed)

        self.userRepository.save(user)
        self.auditNotifier.notify("REGISTER", {"email": email})

        return {"message": "User registered"}

    def loginUser(self, email: str, password: str) -> str:
        user = self.userRepository.findByEmail(email)
        if not user or not self.passwordHasher.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")

        token = self.jwtSigner.sign(user.id)
        self.auditNotifier.notify("LOGIN", {"user_id": user.id})
        return token

    def validateToken(self, token: str) -> int:
        user_id = self.jwtSigner.verify(token)
        return user_id

    def requestPasswordReset(self, email: str):
        user = self.userRepository.findByEmail(email)
        if not user:
            raise ValueError("User not found")

        token_hash = self.passwordHasher.hash(email + "reset")
        user.reset_token_hash = token_hash

        self.userRepository.update(user)
        self.auditNotifier.notify("RESET_REQUEST", {"email": email})

        return {"reset_token": token_hash}

    def resetPassword(self, token: str, newPass: str):
        user = self.userRepository.findByResetToken(token)
        if not user:
            raise ValueError("Invalid token")

        user.password_hash = self.passwordHasher.hash(newPass)
        user.reset_token_hash = None

        self.userRepository.update(user)
        self.auditNotifier.notify("RESET_PASSWORD", {"user_id": user.id})

        return {"message": "Password updated"}