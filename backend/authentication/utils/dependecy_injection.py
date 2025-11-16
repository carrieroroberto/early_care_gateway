from ..repositories.user_repository import UserRepositoryImpl
from ..utils.hasher import PasswordHasher
from ..utils.jwt_signer import JwtSigner
from ..utils.audit_notifier import AuditClient
from ..services.authentication_service import AuthenticationService

user_repository = UserRepositoryImpl()
password_hasher = PasswordHasher()
jwt_signer = JwtSigner(secret="my-secret")
audit_notifier = AuditClient()

auth_service = AuthenticationService(
    userRepository=user_repository,
    auditNotifier=audit_notifier,
    passwordHasher=password_hasher,
    jwtSigner=jwt_signer
)

def get_auth_service():
    return auth_service