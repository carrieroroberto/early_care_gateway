from datetime import datetime, timedelta
import jwt

class JwtSigner:
    def __init__(self, secret, expires_minutes):
        self.secret = secret
        self.expires = expires_minutes

    def sign(self, user_id: int) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=self.expires)
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify(self, token: str) -> int:
        payload = jwt.decode(token, self.secret, algorithms=["HS256"])
        return payload["sub"]