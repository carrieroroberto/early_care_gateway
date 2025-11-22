from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)