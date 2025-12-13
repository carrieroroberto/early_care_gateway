from datetime import datetime, timezone, timedelta
from typing import Dict
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

class JwtSigner:
    """
    Utility class for creating and verifying JSON Web Tokens (JWT).
    Uses HS256 algorithm for signing.
    """
    def __init__(self, secret: str, expires_minutes: int = 60):
        self.secret = secret
        self.expires_minutes = expires_minutes

    def create_token(self, doctor_id: str, name: str, surname: str) -> str:
        """
        Generates a new JWT token for a given doctor.
        Payload includes doctor_id, name, surname, and expiration time.
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expires_minutes)
        payload = {
            "sub": doctor_id,
            "name": name,
            "surname": surname,
            "exp": expire
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_token(self, token: str) -> Dict:
        """
        Decodes and verifies a JWT token.
        Raises exceptions if the token is expired or invalid.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload

        except ExpiredSignatureError:
            raise Exception("Token has expired")

        except InvalidTokenError:
            raise Exception("Invalid token")