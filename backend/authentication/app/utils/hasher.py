# Import CryptContext from passlib to handle password hashing
from passlib.context import CryptContext

# Configure the context to use bcrypt for hashing
# deprecated="auto" ensures older schemes can still be verified but new hashes use the current scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:
    """
    Utility class for hashing and verifying passwords using bcrypt.
    """
    def hash(self, password: str) -> str:
        """
        Hashes a plain text password.
        """
        return pwd_context.hash(password)

    def verify(self, plain: str, hashed: str) -> bool:
        """
        Verifies a plain text password against a hashed string.
        Returns True if they match, False otherwise.
        """
        return pwd_context.verify(plain, hashed)