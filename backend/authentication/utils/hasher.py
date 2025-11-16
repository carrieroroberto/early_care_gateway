from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, password: str, hash_value: str) -> bool:
        return pwd_context.verify(password, hash_value)