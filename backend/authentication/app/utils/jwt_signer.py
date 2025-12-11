import jwt
from datetime import datetime, timezone, timedelta
from jwt import ExpiredSignatureError, InvalidTokenError
from typing import Dict

class JwtSigner:
    """
    Utility class for creating and verifying JSON Web Tokens (JWT).
    Uses HS256 algorithm for signing.
    """
    def __init__(self, secret: str, expires_minutes: int = 30):
        self.secret = secret
        self.expires_minutes = expires_minutes

    def create_token(self, subject: str) -> str:
        """
        Generates a new JWT token for a given subject (e.g., user ID).
        Sets the expiration time based on the configuration.
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expires_minutes)
        payload = {"sub": subject, "exp": expire}
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